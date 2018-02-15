import EFZP as zp
p = zp.parse('''
Apply Here<https://www.firstnaukri.com/job-listings-Sales-Application-Engin=
eer-jobs-in-Bengaluru-Bangalore-Chennai-Delhi-Pune-in-Keyence-India-Private=
-Limited-030118600027>


Dear Candidate,

Greetings from Firstnaukri!

This is regarding a Pooled Campus Drive Pan India for hiring B.E/B.Tech can=
didates graduating in 2018 as =E2=80=9CSales Application Engineers (SAE)=E2=
=80=9D for one of our esteemed client, =E2=80=9CKeyence India Pvt Ltd=E2=80=
=9D.

Please click on this link to the =E2=80=9CWelcome & Registration Page=E2=80=
=9D for all necessary details:
URL: https://www.firstnaukri.com/careers/customised/landingpage/keyence/412=
018/index.html

Please note that =E2=80=9COnly Male Candidates can apply=E2=80=9D

=E2=80=9CInstructions & Guidelines=E2=80=9D to be followed by the candidate=
s for registration:

=E2=80=A2 Candidates will be asked to enter the Email ID (which can be used=
 by you as your username while you appear for 'Online Test') and set a pass=
word for yourself at the time of application. Please enter a Valid Email ID=
 & Password that you can easily remember.

=E2=80=A2 Please recheck the spelling of your email twice after entering. (=
Common mistakes committed by candidates during registration are entering 'g=
amil' instead of 'gmail', 'yaho instead of yahoo'=E2=80=A6etc)

=E2=80=A2 Please make a note of the 'Email ID' that you are entering, the '=
Password' that you are setting for yourself and all the other details that =
you are entering at the time of registration (Eg: Details such as Date of B=
irth, Marks, Address=E2=80=A6etc) in a separate document for your reference=
. These are crucial data required to be entered again during your Online Te=
st for the test to start.

=E2=80=A2 Candidates need to compulsorily upload their =E2=80=9CUpdated Res=
ume/CV=E2=80=9D while registering.

=E2=80=A2 The =E2=80=9CUpdated Resume/CV=E2=80=9D needs to be in .jpg, .png=
 or in Word Format & file size not exceeding 400KB.

=E2=80=A2 Please note that candidates will not be shortlisted only based on=
 the =E2=80=9CEligibility Criteria=E2=80=9D mentioned in the =E2=80=9CWelco=
me & Registration=E2=80=9D page but on other important factors too.

=E2=80=A2 The Shortlisted candidates will have to appear for an Online Test=
 which will be communicated.

During the registration process, if the candidates have any doubts, all the=
 doubts in a campus can be consolidated and emailed to 'arpith.dsouza@first=
naukri.com' (OR) any one of the following helpline numbers can be called be=
tween 10am to 5:30PM from Monday to Friday: 080 - 40439004 We recommend ema=
ils than phone calls and queries raised over emails will be resolved within=
 24 hours.

Thanks for your support in advance!!

With Regards,
For Keyence India,
Firstnaukri Team.


Apply Here<https://www.firstnaukri.com/job-listings-Sales-Application-Engin=
eer-jobs-in-Bengaluru-Bangalore-Chennai-Delhi-Pune-in-Keyence-India-Private=
-Limited-030118600027>


Disclaimer:The sender of this email is registered with Firstnaukri.com as K=
eyence India Private Limited ( SKCL-ICON, 3rd Floor, C-42 & C-43, CIPET Roa=
d, Thiru-Vi-Ka Industrial Estate,Guindy, 75, 29 - 600032) using Firstnaukri=
.com services. The responsibility of checking the authenticity of offers/co=
rrespondence lies with you.

If you consider the content of this email inappropriate or spam, you may re=
port abuse by forwarding this email to: abuse@firstnaukri.com<mailto:abuse@=
firstnaukri.com>

Please note that Firstnaukri.com does NOT endorse any requests for money pa=
yments, or sharing of bank account details.
	''')
print (str(p['body']), " \n\n\n", str(p['reply_text']))

