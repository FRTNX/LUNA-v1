# LUNA
### NB: Major refactor in progress. Please report all bugs to frtnx@protonmail.com or open a new issue.
[![Join the chat at https://gitter.im/LUNA-research-tool/community](https://badges.gitter.im/LUNA-research-tool/community.svg)](https://gitter.im/LUNA-research-tool/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Luna is a terminal based research tool.

## Demo
![](lunademo.gif)


## Installation (Linux)

Please note that these instructions are for ubuntu 16.04 but should work for most other distributions. If you encounter any issues during installation please send a stack trace to the email provided at the bottom of this readme or open an issue.

Choose the directory you would like to keep the code in.
Please note that after setup is complete, moving this directory will break the launcher,
so store the code in a place you wont disturb.

Inside your chosen directory run:

```git clone https:github.com/FRTNX/LUNA```

Then

```cd LUNA```

```python3 setup.py```

This will will create a launcher and install dependecies. After the process completes it will automatically launch an instance of Luna. To run Luna in future simply open a terminal and enter

```luna```


[![Alt text](data/media/screenshot.png?raw=true "Screenshot of Luna")](https://github.com/FRTNX/LUNA/blob/master/data/media/screenshot.png)


## User guide

After you have been prompted for a code name a help guide may be obtained by typing in

```help```

This will show you a few useful commands to help get you started.

The program is feature rich and all though free text is accepted and processed accordingly, the most exciting activities are key word activated.


[![Alt text](data/media/screenshot4.0.png?raw=true "Screenshot of Luna 2")](https://github.com/FRTNX/LUNA/blob/master/data/media/screenshot4.png)


## Philosophy, Challenges, and Road Map

Luna is first and foremost a research tool. She may have conversational ability but that takes a second place. The philosphy here is a research tool that is

 - light weight
 - capable of delivering information offline or online
 - anonymous with its web interactions
 - data efficient, no cache, css, or unnecessary data. Only what you need.

Most of these objectives have already been met to some degree save for anonymity. I have chosen to use proxychains to handle all internet interactions. Due to the unavailability of time, I have not made good on this idea. What I currently see as the biggest challenge, perhaps naively, is how to manage the proxy servers list, ensuring that all requests go through an elite node first, and mitigating the latency this may cause.

This program uses a terminal client in front of a mongodb database. The current database loaded upon install is rather heavy. To mitigate this, a batch of smaller initial databases will be released, along with some logic that will install a database best suited to the host machines resources. Improvements will continually be made to make it lighter still.


[![Alt text](data/media/screenshot2.png?raw=true "Screenshot of Luna 2")](https://github.com/FRTNX/LUNA/blob/master/data/media/screenshot2.png) [![Join the chat at https://gitter.im/LUNA-research-tool/community](https://badges.gitter.im/LUNA-research-tool/community.svg)](https://gitter.im/LUNA-research-tool/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Contributions are welcome.

Please report all bugs to frtnx@protonmail.com
