# Network Security Basics

## What is Network Security?

Network security protects the integrity, confidentiality, and availability of computer networks and data. It includes both hardware and software technologies.

## Key Concepts

### 1. CIA Triad

The foundation of information security:

- **Confidentiality**: Only authorized users access data
- **Integrity**: Data is accurate and hasn't been tampered with
- **Availability**: Systems and data are accessible when needed

### 2. Defense in Depth

Multiple layers of security controls:
- If one layer fails, others still provide protection
- "Don't put all your eggs in one basket"

## Core Network Security Tools

### Firewalls

**What they do:**
- Monitor and control incoming/outgoing network traffic
- Based on predetermined security rules
- Act as a barrier between trusted and untrusted networks

**Types:**
1. **Packet-filtering firewalls** - Basic, checks packet headers
2. **Stateful inspection firewalls** - Tracks connection state
3. **Proxy firewalls** - Application-level gateway
4. **Next-generation firewalls (NGFW)** - Deep packet inspection, IPS

**Best practices:**
- Default deny policy (block everything, allow only necessary)
- Regular rule review and cleanup
- Log all denied connections
- Keep firmware updated

### Virtual Private Networks (VPNs)

**What they do:**
- Encrypt internet connection
- Hide IP address and location
- Create secure tunnel for data transmission

**Use cases:**
- Remote work access to company network
- Secure public Wi-Fi usage
- Bypass geo-restrictions (use responsibly)
- Privacy protection

**Types:**
1. **Site-to-Site VPN** - Connects entire networks
2. **Remote Access VPN** - Individual users connect to network
3. **SSL VPN** - Browser-based, no client software needed

**VPN Protocols:**
- **OpenVPN** - Open-source, highly secure
- **WireGuard** - Modern, fast, lightweight
- **IKEv2/IPSec** - Fast, good for mobile
- ❌ **PPTP** - Obsolete, insecure (avoid)

### Intrusion Detection/Prevention Systems (IDS/IPS)

**IDS (Intrusion Detection System):**
- Monitors network for suspicious activity
- Alerts administrators
- Passive monitoring

**IPS (Intrusion Prevention System):**
- Monitors AND takes action to block threats
- Active protection
- Can automatically block malicious traffic

**Detection methods:**
1. **Signature-based** - Matches known attack patterns
2. **Anomaly-based** - Detects deviation from normal behavior
3. **Hybrid** - Combines both methods

### Network Segmentation

**Concept:**
Divide network into smaller, isolated segments.

**Benefits:**
- Limits lateral movement of attackers
- Contains breaches to specific segments
- Easier to monitor and manage
- Compliance with regulations (PCI-DSS, HIPAA)

**Common segments:**
- **DMZ (Demilitarized Zone)** - Public-facing services
- **Internal network** - Employee workstations
- **Management network** - IT administration
- **Guest network** - Visitor Wi-Fi (isolated from internal)

## Secure Network Design Principles

### 1. Principle of Least Privilege
- Users/systems only get minimum necessary access
- Reduces attack surface
- Limits damage from compromised accounts

### 2. Zero Trust Architecture
- "Never trust, always verify"
- Verify every access request, regardless of location
- No implicit trust based on network location

### 3. Network Access Control (NAC)
- Authenticate devices before network access
- Check device compliance (antivirus, patches)
- Quarantine non-compliant devices

## Common Network Attacks

### 1. Man-in-the-Middle (MitM)
Attacker intercepts communication between two parties.

**Protection:**
- Use HTTPS everywhere
- VPN for public Wi-Fi
- Certificate pinning

### 2. Denial of Service (DoS/DDoS)
Overwhelm system with traffic, making it unavailable.

**Protection:**
- DDoS mitigation services (Cloudflare, AWS Shield)
- Rate limiting
- Traffic filtering

### 3. ARP Spoofing
Attacker sends fake ARP messages to redirect traffic.

**Protection:**
- Static ARP entries for critical hosts
- ARP spoofing detection tools
- Network segmentation

### 4. DNS Hijacking
Redirect DNS queries to malicious sites.

**Protection:**
- Use secure DNS (DNS over HTTPS)
- DNSSEC validation
- Monitor DNS logs

## Wi-Fi Security

### Encryption Standards:
- ❌ **WEP** - Broken, never use
- ❌ **WPA** - Deprecated
- ⚠️ **WPA2** - Vulnerable to KRACK attack, still acceptable
- ✅ **WPA3** - Current standard, use when available

### Wi-Fi Best Practices:
1. **Strong passphrase** (20+ characters)
2. **Disable WPS** (easy to crack)
3. **Hide SSID** (security through obscurity, minor benefit)
4. **MAC filtering** (weak protection, but adds layer)
5. **Guest network** (isolated from main network)
6. **Regular firmware updates**

## Monitoring and Logging

**What to log:**
- Failed login attempts
- Firewall denials
- IDS/IPS alerts
- VPN connections
- Administrative actions
- DNS queries

**Log management:**
- Centralized logging (SIEM - Security Information and Event Management)
- Regular review and analysis
- Retention policy (typically 90 days minimum)
- Alerts for suspicious patterns

## Network Security Checklist

- [ ] Firewall configured with default-deny policy
- [ ] VPN for remote access
- [ ] IDS/IPS deployed and monitored
- [ ] Network segmentation implemented
- [ ] Wi-Fi using WPA2 or WPA3
- [ ] Regular security audits and penetration testing
- [ ] Patch management process
- [ ] Centralized logging and monitoring
- [ ] Incident response plan documented
- [ ] Employee security awareness training

---

**Last updated:** October 2024
