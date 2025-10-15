# Incident Response Guide

## What is an Incident?

A security incident is any event that compromises the confidentiality, integrity, or availability of information assets.

**Examples:**
- Data breach / unauthorized access
- Malware infection (ransomware, virus)
- Phishing attack success
- DDoS attack
- Insider threat
- Lost/stolen device with sensitive data

## Why Incident Response Matters

**Statistics:**
- Average time to identify a breach: 207 days (IBM)
- Average time to contain a breach: 73 days
- Average cost of a data breach: $4.45M
- **Fast response reduces costs by up to 30%**

## The Incident Response Lifecycle

### Phase 1: Preparation

**BEFORE an incident happens:**

1. **Create IR Plan**
   - Define roles and responsibilities
   - Contact lists (internal team, external partners, law enforcement)
   - Communication templates
   - Escalation procedures

2. **Assemble IR Team**
   - Incident Response Manager
   - Security Analysts
   - IT Operations
   - Legal/Compliance
   - Communications/PR
   - Management

3. **Set Up Tools**
   - Logging and monitoring (SIEM)
   - Forensic tools
   - Backup systems
   - Communication channels (encrypted chat)

4. **Training**
   - Regular tabletop exercises
   - Simulate different incident types
   - Test IR plan quarterly

5. **Documentation**
   - Network diagrams
   - Asset inventory
   - Data flow maps
   - Baseline normal activity

### Phase 2: Detection and Analysis

**Identify and assess the incident:**

1. **Detection Sources**
   - IDS/IPS alerts
   - Antivirus alerts
   - SIEM correlation
   - User reports
   - Anomaly detection
   - Third-party notification

2. **Initial Triage**
   - Is this a real incident or false positive?
   - What type of incident?
   - What systems/data are affected?
   - How severe is it?

3. **Severity Classification**

   **Critical (P1):**
   - Active data breach
   - Ransomware encrypting critical systems
   - Production systems down
   - **Response time: Immediate**

   **High (P2):**
   - Confirmed malware on multiple systems
   - Successful phishing with credential compromise
   - **Response time: Within 1 hour**

   **Medium (P3):**
   - Isolated malware infection
   - Attempted intrusion (blocked)
   - **Response time: Within 4 hours**

   **Low (P4):**
   - Policy violations
   - Suspicious but unconfirmed activity
   - **Response time: Next business day**

4. **Gather Evidence**
   - Take screenshots
   - Capture memory dumps
   - Preserve logs (don't modify originals)
   - Document everything with timestamps
   - Chain of custody for potential legal action

### Phase 3: Containment

**Stop the incident from spreading:**

1. **Short-term Containment**
   - Isolate affected systems (disconnect from network, NOT power off)
   - Block malicious IPs/domains at firewall
   - Disable compromised accounts
   - Implement emergency ACLs

2. **Long-term Containment**
   - Apply temporary fixes
   - Move systems to isolated VLAN for analysis
   - Implement additional monitoring
   - Prepare for recovery

**Important:** Balance containment with business continuity. Coordinate with management.

### Phase 4: Eradication

**Remove the threat:**

1. **Identify Root Cause**
   - How did the attacker get in?
   - What vulnerability was exploited?
   - Were there multiple entry points?

2. **Remove Malware**
   - Anti-malware scans
   - Manual removal if needed
   - Check for persistence mechanisms

3. **Close Vulnerabilities**
   - Apply patches
   - Change compromised credentials (ALL of them)
   - Update firewall rules
   - Fix misconfigurations

4. **Verify Eradication**
   - Rescan systems
   - Monitor for reinfection
   - Check for backdoors

### Phase 5: Recovery

**Restore normal operations:**

1. **Restore Systems**
   - From clean backups (verify backups aren't infected)
   - Rebuild if necessary (may be safer than cleaning)
   - Test thoroughly before production

2. **Gradual Restoration**
   - Start with least critical systems
   - Monitor closely for issues
   - Staged return to full operations

3. **Enhanced Monitoring**
   - Temporary increased logging
   - Watch for signs of reinfection
   - Continue for at least 30 days

4. **Validation**
   - Confirm systems are clean
   - Test functionality
   - User acceptance testing

### Phase 6: Lessons Learned

**Post-incident review (within 2 weeks):**

1. **Post-Mortem Meeting**
   - What happened? (timeline)
   - What was done well?
   - What could be improved?
   - Were procedures followed?

2. **Update Documentation**
   - Revise IR plan based on lessons
   - Update runbooks
   - Document new attack techniques observed

3. **Implement Improvements**
   - Fix identified weaknesses
   - Deploy additional controls
   - Update monitoring rules
   - Additional training if needed

4. **Share Knowledge**
   - Inform relevant teams
   - Update threat intelligence
   - Share with industry peers (anonymized)

## Communication During Incidents

### Internal Communication
- **Status updates**: Every 4 hours minimum during active incident
- **Use secure channels**: Encrypted chat, not compromised email
- **Be factual**: Stick to known facts, avoid speculation
- **Management**: Keep updated on severity, impact, estimated resolution

### External Communication
- **Legal/Compliance**: May be required to notify regulators
- **Customers**: Transparency builds trust, but coordinate with legal
- **Law Enforcement**: For criminal activity, coordinate with legal
- **Media**: Only designated spokesperson, approved messaging

### Notification Requirements

**GDPR (EU):**
- Notify regulator within 72 hours of becoming aware
- Notify affected individuals if high risk

**CCPA (California):**
- Notify affected individuals without unreasonable delay

**HIPAA (Healthcare):**
- Notify HHS within 60 days if 500+ individuals affected

**Check your jurisdiction and industry requirements!**

## Common Mistakes to Avoid

1. **Powering off infected systems** - Loses volatile memory evidence
2. **Not preserving logs** - Critical for forensics
3. **Acting without plan** - Can make things worse
4. **Poor communication** - Creates confusion and panic
5. **Ignoring legal/compliance** - Can result in fines
6. **No documentation** - Can't learn from incident
7. **Premature "all clear"** - Attacker may still have access

## Incident Response Tools

### Detection & Monitoring
- **SIEM**: Splunk, ELK Stack, QRadar
- **EDR**: CrowdStrike, Carbon Black, SentinelOne
- **Network monitoring**: Wireshark, Zeek, Suricata

### Forensics
- **Disk imaging**: FTK Imager, dd
- **Memory analysis**: Volatility, Rekall
- **File analysis**: Autopsy, Sleuth Kit

### Malware Analysis
- **Sandboxes**: Cuckoo, Any.Run
- **Static analysis**: PEStudio, strings, VirusTotal

### Communication
- **Encrypted chat**: Signal, Wickr
- **Secure email**: PGP-encrypted

## Practice Makes Perfect

**Run tabletop exercises quarterly:**

**Scenario examples:**
1. Ransomware encrypts file servers
2. Phishing compromises CEO email
3. DDoS takes down website
4. Insider exfiltrates customer data
5. Zero-day exploit in web application

**Test:**
- Can team be reached?
- Do they know their roles?
- Is documentation accessible?
- Are communication channels working?
- Can you recover from backups?

---

**Last updated:** October 2024
