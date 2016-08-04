# tjekjobnet
Automatically check the semi random jobs suggested at jobnet.dk. Please check full post at [my personal site](http://mtherkildsen.dk/post/automatic-job-check-at-jobnet-dk/ "Title")

# Config.json
This file is basically the only thing you need to configure. Input the necessary fields and you are good to go. If the automatic check fails for some reason, an email is send to the specified address to inform you (requires access to a mail server, e.g. asmtp.something.whatever)

# Add to crontab
After configuring and testing, make sure to setup the script to run automatically.

```shell
crontab -e
```

to run script everyday at 8 am/pm issue
```shell
0 8,20 * * * python /home/pi/jobnet/tjekjobnet.py &
```
