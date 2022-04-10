# ThreeFactorAuthentication

Almost all websites including Financial Institutions/ social media accounts provides two-factor authentication
The two mechanisms used are:
1) Knowledge Based Authentiation : Typically Username and Password
2) Possession Based Authentication : A One Time Password (OTP) is sent/generated on Mobile/Device 

Possession Based Authentication cannot protect unauthorized access if:
a) Trusted Device in hands of malicious hands
b) SIM-Fraud
c) Saving (Autofill) password on Trusted Devices using Password Manager
d) “Remember Me” on Trusted Device.

Three factor authentication uses Face Recognition in conjunction with the exisiting two factor Authentication mechanism
The three factor authenication begins by capturing the image of user using the Web-cam/Front Camera.

It has 5 phases:
1) Capture
2) Detect
3) Identify
4) Persist
5) Report

This prototype is written in Python and uses OpenCV, TensorFlow machine learning libraries and SQLLite Database for persistance and report generation

Benefits:
* Protects applications from unauthorized usage
* It generates Suspicious Activity Report for failed Login Attempts.
* In the Suspicious Activity Report the picture of the attacker is available which can be used by law enforcement officials

## Presentation Video:
![video](Demo/Three Factor Authentication.mp4)
