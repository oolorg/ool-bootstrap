ool-bootstrap
=============
The Bootstrap will you automatically built the verification environment of
networks using SDN mainly.

* Make the automatic construction of the network and VM using the Heat.
* The Bootstrap will run in the controller node. And it also works as web server.
* Show test results from on Bootstrap.

Requirements
-----------------------
* OpenStack (Grizzly)
  - neutron
  - nova
  - heat
  - glance

Install
-----------------------
You will follow the steps below to install the bootstrap.

Bootstrap:

    git clone https://github.com/ool-taku/ool-bootstrap.git
    tar zvf package-ool-bootstrap.tar.gz
    package-ool-bootstrap/bootstrap/install.sh
    vi /usr/lib/ool-test/bootstrap/settings/credentials

Apache:

    - ports.conf
      Listen 0.0.0.0:18080
      NameVirtualHost 0.0.0.0:18080
      ※ port number rewrite as arbitrarily.


Test Scenario
-----------------------
Test Scenario is composed of one Master App and plural of  server and Agent Apps servers. Master server manages all Agents. Agent App free format.The format of Master App is shown below.

 - “verify.py” has the interface between bootstrap, so don’t change it.
 - Write verification code in execute.py.
 - Interface between Master and Agents is not defined.
 - Write the result to HTML file named “result.html”.

The code for each application, must be written in JSON format.
Additionally, write in Heat Template be additional packages and server environment in Heat Template, 

Sample codes　are stored in a folder the following .

    bootstarp/ool-test/bootstrap/templates

* Sample Scenario

 - Ping
 - iPerf
 - Neutron LBaaS (Load-balancer-as-a-Service)


Configuration environment
-----------------------

Basic architecture：

        +---------------+                                                  
        |Controller Node|                                                  
        | - Neutron     |                                                  
        | - Nova        |         +---------------+   +---------------+    
        | - Heat        |         | Compute Node  |   | Compute Node  |    
        | - Glance      |         | - nova-compute|   | - nova-compute|    
        | - Bootstrap   |         | - *-agent     |   | - *-agent     |    
        +---------------+         +---------------+   +---------------+    
                |                         |                   |            
                +-----------+-------------+-------------------+            
                            |                                              
                      +-----+-----+                                        
                      |  SDN Box  |                                        
                      +-----------+                                        

Test architecture:

 Maybe later...


Notes
-----------------------
