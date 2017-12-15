pd-iot-doorbell
======

Press an AWS IoT button, get paged via [PagerDuty](https://www.pagerduty.com/)

### WHY would I do this?
Technically, it was fun to figure out how AWS IoT works. I'm sure I will
appreciate this reference in the future because AWS IoT is full of new terms
that I haven't used before.

Practically, I live in an apartment and we don't have a doorbell. In the past,
the :pizza: delivery just drove off because they didn't have my cell number.
:imp:

But why not just use AWS SNS or Twilio directly? I could have, but there are
multiple people that live here and it might be nice to utilize PagerDuty
schedule overrides or other features without updating the Lambda Function.

### End Result
![Screenshot](https://raw.githubusercontent.com/jolexa/pd-iot-doorbell/master/screenshot.png)

#### Deploy
1. Configure your [AWS IoT button](https://www.amazon.com/dp/B01KW6YCIM) via
[documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)
provided (There is no automated way to do this, as far as I know)
2. Add an attribute to your IoT Thing for the serial number: `"serial":"<insert serial
number here>"` -- This is used for discovery later
3. Change Variables for your AWS Account:
[Makefile#L1-L5](https://github.com/jolexa/pd-iot-doorbell/blob/master/Makefile#L1-L5)
4. Deploy CloudFormation Template: `make deploy`
5. Configure a PagerDuty Service, Escalation Policy, etc
https://community.pagerduty.com/t/the-onboarding-checklist/475
6. Add EC2 Parameter store secret in the region deployed that has the path:
`/pd-iot-button/service_key` with the `service_key` setup in previous step
7. Press the button, get paged, eat :pizza::exclamation:

#### Questions / Contact
I doubt that I will update this often, but I always watch GitHub Issues or Pull
Requests. Feel free to reach me on [Twitter](https://twitter.com/jolexa) as
well.
