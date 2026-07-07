---
id: 20457820922011
brand: "Parallel Help Center"
brand_id: 7011641908507
locale: "en-us"
title: "Parallel Firewall Configuration and Testing Guide"
category: "School Tech Support Hub"
section: "Tech Setup and Support"
labels: []
author: "Permanently deleted user"
created_at: "2023-11-16T20:14:22Z"
updated_at: "2026-05-19T13:19:48Z"
url: "https://help.parallellearning.com/hc/en-us/articles/20457820922011-Parallel-Firewall-Configuration-and-Testing-Guide"
---
# Parallel Firewall Configuration and Testing Guide

**Last Updated April 2025**

There are three steps you will need to complete to ensure that Parallel Providers can successfully conduct telehealth sessions with your school’s students. These steps include configuring your school’s firewall, reviewing system requirements, and performing a successful connection test.

Step 1: [Firewall configuration](https://help.parallellearning.com/hc/en-us/articles/20457820922011/#Step_1)

Step 2: [Review of Parallel System Requirements](https://help.parallellearning.com/hc/en-us/articles/20457820922011/#Step_2)

Step 3: [Complete a Connection Test](https://help.parallellearning.com/hc/en-us/articles/20457820922011/#Step_3)

[Troubleshooting Telehealth Sessions with Students](https://help.parallellearning.com/hc/en-us/articles/20457820922011/#Troubleshooting)

### **Step 1 - Firewall Configuration**

To enable our telehealth services, your network firewall will need to allow outbound traffic to our video chat providers. Our platform integrates three core technologies: Agora (whiteboard functionality), Surfly (co-browsing capabilities), and Daily (video conferencing). While most network traffic routes through proxies within our domain, some school firewalls require specific configuration to ensure seamless service delivery. The following firewall settings will guarantee uninterrupted access to all teleconferencing features at your school.

**1️⃣ -** [**Review and follow the instructions in this link**](https://www.notion.so/Configuring-corporate-networks-firewalls-and-VPN-settings-9fb069b923db479586d7c14085c69a7f?pvs=21) (external link maintained by Daily, our video chat provider)

2️⃣ **-** Enable the following Domains:

```
*.agora.io
*.sd-rtn.com
*.edge.agora.io
*.edge.sd-rtn.com
web-1.ap.sd-rtn.com
web-2.ap.sd-rtn.com
ap-web-1.agora.io
ap-web-2.agora.io
webcollector-rtm.agora.io
logservice-rtm.agora.io
rtm.statscollector.sd-rtn.com
rtm.logservice.sd-rtn.com
*.stream-io-api.com
parallel-prod.uc.r.appspot.com
*.surfly.com
cobrowsing.parallellearning.com
*.parallellearning.com
```

3️⃣ **-** Enable the following Ports (Note: These ports go with the Agora Domains above):

|  |  |  |
| --- | --- | --- |
| Destination ports | Port type | Operation |
| 80; 443; 3433; 4700 - 5000; 5668; 5669; 6080; 6443; 8667; 9591; 9593; 9601; 9667; 30011 - 30013 | TCP | Allow |
| 3478; 4700 - 5000; 10000-20000 | UDP | Allow |

#### **Before you continue, make sure that you've completed all three parts to this step:**

⭐️ Enable Daily domain [**(per instructions at this link)**](https://www.notion.so/Configuring-corporate-networks-firewalls-and-VPN-settings-9fb069b923db479586d7c14085c69a7f?pvs=21)

⭐️ Enable domains listed above

⭐️ Enable ports listed above

### **Step 2 - Parallel System Requirements**

To ensure that our tools operate smoothly for your students, please review the following system requirements:

|  |  |
| --- | --- |
| Browsers | Parallel supports the two most recent versions of Chrome or Safari  Chrome: <https://www.google.com/chrome/update/>  Safari: <https://support.apple.com/en-us/HT204416> |
| Devices | Parallel is designed to run on devices with a minimum screen resolution of 1280x720.  For assessment services, students must use a laptop or desktop computer. **Assessment services are incompatible with tablets or iPads per clinical requirements.** |
| Bandwidth | The recommended minimum bandwidth to support Parallel tele-sessions is 5 mbps upload and 5 mbps download |
| User Tips | Each student should join on a separate device to maximize video clarity. Students should use headphones to minimize echo. |

### **Step 3 - Connection Test**

This connection test will verify that the network in your school building has been successfully set up and Parallel Telehealth sessions can now be conducted over your school’s network. The test takes about 5-10 minutes to complete. Please reach out to your Customer Success Manager if you have any questions or encounter any issues during the test.

1. Navigate to <https://telehealth.parallellearning.com/connection-test> with the browser type the students will be using for their sessions.
2. Once on the website, please log in using the test credentials shared with you via email. Please contact your Customer Success Manager if you would like the test credentials resent to you.

![](https://help.parallellearning.com/hc/article_attachments/22143839090331)

3. Upon signing in, you may be asked to give permission to your browser to access your camera and microphone - be sure to allow each. Begin the connection test by clicking on the “Check Connection” link under the media preview section of the webpage as shown below:

   ![Screenshot 2025-08-07 at 4.25.32 PM.png](https://help.parallellearning.com/hc/article_attachments/39789078610075)
4. You will see several boxes of each service that is being tested with the services names appearing gray while the test is still in progress. The names will appear green when the test has completed and all services have passed successfully. A warning symbol will appear if any services fail the test.

**ℹ️ Note** Please note that it may take up to 2-3 minutes for the test to complete depending on your network speed and system requirements. If the services names remain gray after 2-3 minutes, this indicates the test was unable to complete and could be a result of internet connectivity issues. We recommend checking your network connection and restarting the test.

*Example of a connection test in progress*

![Screenshot 2025-08-07 at 4.26.18 PM.png](https://help.parallellearning.com/hc/article_attachments/39789078612507)

*Example of a completed connection test:*

![Screenshot 2025-08-07 at 4.26.14 PM.png](https://help.parallellearning.com/hc/article_attachments/39789078613787)

*Example of a service that has failed the connection test:*

![Screenshot 2025-08-07 at 4.29.38 PM.png](https://help.parallellearning.com/hc/article_attachments/39789068937755)

6. Once you receive green checks for ALL services once the connection test has completed, send a screenshot of the results to your Customer Success Manager to verify the success of the test.
7. If you receive a warning symbol for any of the services in the connection test, please refer to the table below for further troubleshooting.

|  |  |
| --- | --- |
| **If this test fails…** | **…try the following** |
| Parallel Meeting Server | * Double check school firewall, content filters, etc. to make sure it follows allowlist |
| Meeting Sync Service | * Double check school firewall, content filters, etc. to make sure it follows allowlist |
| Media Streaming Service | * Double check school firewall, content filters, etc. to make sure it follows allowlist * Close any other programs/tabs using the device's mic or camera * Double check to ensure that device's mic and camera are working. (Further [troubleshooting options here](https://help.parallellearning.com/hc/en-us/articles/18322789020187#h_01HBXN543SFW5GNY1B3RN8YV18)) |
| Whiteboard Service | * Please contact your Customer Success Manager |
| Chat Service | * Please contact your Customer Success Manager |
| Network Quality | * Check your internet speed to ensure that it meets Parallel’s minimum requirements * If not, confirm that the device is connected to the correct WiFi network, explore Ethernet connection. (Further [troubleshooting options here](https://help.parallellearning.com/hc/en-us/articles/18322789020187#h_01HBXN543SFW5GNY1B3RN8YV18)) |

8. If you’ve performed the above troubleshooting steps and are still encountering issues, please contact your Customer Success Manager with a brief description of the issue so they may put you in contact with our product engineering team for troubleshooting.

### **Troubleshooting Telehealth Sessions with Students**

Once telehealth sessions have begun, we recommend referring to our [Troubleshooting Common Technical Issues Guide](https://help.parallellearning.com/hc/en-us/articles/18322789020187) if any facilitators or students encounter any issues with their sessions. If the issues persist, please contact [support@parallelearning.com](mailto:support@parallelearning.com) with a brief description of the issue for further assistance and engineering support.
