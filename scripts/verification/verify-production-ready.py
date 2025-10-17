#!/usr/bin/env python3
"""
Universal Production Readiness Verification Framework
Compatible with any project, language, or stack
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class UniversalVerifier:
    def __init__(self, sprint_number: Optional[str] = None):
        self.project_root = Path.cwd()
        self.config = self.load_config()
        self.sprint_number = sprint_number or self.detect_sprint_number()
        
        # Issue counters
        self.critical_count = 0
        self.high_count = 0
        self.medium_count = 0
        self.low_count = 0
        
        # Report
        self.report_lines = []
        
    def load_config(self) -> Dict:
        """Load project configuration"""
        config_file = self.project_root / ".verification-config.json"
        
        if not config_file.exists():
            print("⚠️ Configuration file not found")
            print("Run: ./setup-verification.sh")
            sys.exit(1)
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def detect_sprint_number(self) -> str:
        """Auto-detect sprint number from branch name"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()
            
            # Extract sprint number from branch name
            pattern = self.config["sprints"]["branch_pattern"]
            pattern = pattern.replace("{{N}}", r"(\d+)")
            match = re.search(pattern, branch)
            
            if match:
                return match.group(1)
            
        except:
            pass
            
        print("⚠️ Could not detect sprint number from branch")
        print("Please specify sprint number as argument")
        sys.exit(1)
    
    def get_changed_files(self) -> List[Path]:
        """Get list of changed files in sprint"""
        try:
            # Get base branch for comparison
            base = "main"
            if Path(".verification-config.json").exists():
                with open(".verification-config.json") as f:
                    config = json.load(f)
                    base = config.get("git", {}).get("base_branch", "main")
            
            # Get changed files
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{base}...HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            
            files = []
            for file in result.stdout.splitlines():
                path = Path(file)
                if path.exists():
                    files.append(path)
                    
            return files
            
        except:
            print("⚠️ Could not get changed files")
            print("Falling back to all files in project")
            
            files = []
            for ext in [".py", ".js", ".ts", ".go", ".java"]:
                files.extend(Path(".").rglob(f"*{ext}"))
            return files
    
    def log_issue(self, severity: str, message: str, file: str = None):
        """Log an issue with severity"""
        if severity == "CRITICAL":
            self.critical_count += 1
        elif severity == "HIGH":
            self.high_count += 1
        elif severity == "MEDIUM": 
            self.medium_count += 1
        else:
            self.low_count += 1
            
        line = f"**{severity}:** {message}"
        if file:
            line += f"\nFile: {file}"
        self.report_lines.append(f"\n{line}\n")
        
        print(f"❌ {line}")
    
    def verify_dummy_code(self):
        """Phase 1: Dummy code verification"""
        print("\n" + "="*50)
        print("Phase 1: Dummy Code Detection") 
        print("="*50)
        
        patterns = {
            "python": [
                r'pass\s*$',
                r'raise\s+NotImplementedError',
                r'dummy_\w+',
                r'fake_\w+', 
                r'TODO|FIXME|HACK|XXX',
            ],
            "javascript": [
                r'function\s+\w+\(.*\)\s*{\s*}\s*$',
                r'const\s+\w+\s*=\s*\(\)\s*=>\s*{\s*}\s*$',
                r'throw\s+new\s+Error\(["\']Not implemented["\']\)',
                r'dummy[A-Z]\w*',
                r'fake[A-Z]\w*',
                r'TODO|FIXME|HACK|XXX',
            ]
        }
        
        language = self.config["project"]["language"]
        if language not in patterns:
            print(f"⚠️ No patterns defined for {language}")
            return
        
        files = self.get_changed_files()
        for file in files:
            if not file.exists():
                continue
                
            try:
                content = file.read_text()
                for pattern in patterns[language]:
                    matches = re.finditer(pattern, content, re.MULTILINE)
                    for match in matches:
                        self.log_issue(
                            "HIGH",
                            f"Dummy code pattern detected: {pattern}",
                            str(file)
                        )
            except:
                pass
    
    def verify_security(self):
        """Phase 2: Security verification"""
        print("\n" + "="*50)
        print("Phase 2: Security Verification")
        print("="*50)
        
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        files = self.get_changed_files()
        for file in files:
            if not file.exists():
                continue
                
            try:
                content = file.read_text()
                for pattern in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        self.log_issue(
                            "CRITICAL",
                            f"Hardcoded secret detected: {match.group()}",
                            str(file)
                        )
            except:
                pass
    
    def verify_tests(self):
        """Phase 3: Test verification"""
        print("\n" + "="*50)
        print("Phase 3: Test Verification")
        print("="*50)
        
        language = self.config["project"]["language"]
        test_cmd = self.config.get("language_specific", {}).get(language, {}).get("test_command")
        
        if not test_cmd:
            print(f"⚠️ No test command defined for {language}")
            return
        
        try:
            subprocess.run(
                test_cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Tests passed")
            
        except subprocess.CalledProcessError as e:
            self.log_issue(
                "CRITICAL",
                f"Tests failed with exit code {e.returncode}\n{e.stdout}\n{e.stderr}"
            )
    
    def generate_report(self) -> int:
        """Generate verification report"""
        print("\n" + "="*50)
        print("Generating Report")
        print("="*50)
        
        # Determine status
        if self.critical_count > self.config["thresholds"]["critical_issues_max"]:
            status = "REJECTED"
        elif self.high_count > self.config["thresholds"]["high_issues_max"]:
            status = "REJECTED"
        elif self.medium_count > self.config["thresholds"]["medium_issues_max"]:
            status = "APPROVED WITH OBSERVATIONS"
        else:
            status = "APPROVED"
            
        # Create report file
        report_pattern = self.config["sprints"]["report_pattern"]
        report_file = Path(report_pattern.replace("{{N}}", self.sprint_number))
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        report = f"""# Sprint {self.sprint_number} Verification Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Details
- Name: {self.config['project']['name']}
- Type: {self.config['project']['type']}
- Language: {self.config['project']['language']}

## Issue Summary
- Critical: {self.critical_count} (max {self.config['thresholds']['critical_issues_max']})
- High: {self.high_count} (max {self.config['thresholds']['high_issues_max']})
- Medium: {self.medium_count} (max {self.config['thresholds']['medium_issues_max']})
- Low: {self.low_count}

---

## Issues Detected

{''.join(self.report_lines) if self.report_lines else '✅ No issues detected'}

---

## Final Verdict

**Status:** {status}

Sprint {self.sprint_number} is **{status}**

---

*Report generated by Universal Production Readiness Framework v1.0*
"""
        
        report_file.write_text(report)
        print(f"\n✅ Report generated: {report_file}")
        
        return 0 if status in ["APPROVED", "APPROVED WITH OBSERVATIONS"] else 1
    
    def run(self):
        """Run all verification phases"""
        print(f"\n🔍 Verifying Sprint {self.sprint_number}")
        print(f"Project: {self.config['project']['name']}")
        print(f"Language: {self.config['project']['language']}")
        
        if self.config["verification"]["enable_dummy_detection"]:
            self.verify_dummy_code()
        
        if self.config["verification"]["enable_security_scan"]:
            self.verify_security()
        
        if self.config["verification"]["enable_test_coverage"]:
            self.verify_tests()
        
        return self.generate_report()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Production Readiness Verification')
    parser.add_argument('sprint_number', nargs='?', help='Sprint number to verify')
    parser.add_argument('--setup', action='store_true', help='Setup configuration')
    
    args = parser.parse_args()
    
    if args.setup:
        print("Run: ./setup-verification.sh")
        return 0
    
    verifier = UniversalVerifier(args.sprint_number)
    return verifier.run()


if __name__ == "__main__":
    sys.exit(main())