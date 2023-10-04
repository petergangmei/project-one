
1. Created django project (projectone) with two app #account and #projectone
2. In account app model,  we have provide that is linked to User with Foreignkey field, 
   the profile is generated after User is created with the help of post save signal.
   It also content Password reset model class where I am storing the otp, validity and token etc.
   We also have Projectone App in which we have added Company Model, with a unique slug for having
   unique company identity. 

3. In the home page, I have created hero section with a message and call to action to exlore the top
   companies which is available in the website. The company detail can be view by authenticated user only.

4. User can signup with in the website by providing their email and password. We will send welcome email after 
   a new account has been registered. User will be able to login with their email and password and logout as they wish.

5. User can reset the password by going to forget password page, entered their registered email, if the email is
   available in our database, we will send email with link to reset their account password. This email should be valid
   only for 10 minutes. User will be able to reset account password only once per email.

6. User will be able to access his profile page and update some personal info, and be able to add company from the profile.
   Only the user who have created the company detail will have the permisson to delete the company.

7. API created for all the following functionality:--
   a. 'registere-user' register user by providing email and password in json format. Access token provided on successful registration.
   b. 'login-user' login user if provided correct email and password. Access token provide on successful login.
   c. 'profile' get profile detail of the user, access token required to get profile detail.
   d. 'update-profile' user can update their personal info from here, access token required.
   e. 'user-chage-password' by providing password1, password2, otp and email, password will be updated if correct info is provided.
   f. 'user-password-reset' required email, is provided we will send reset password email.
   g. 'top-companies/<company_type>/' this end point will provide the top companies name list base on "private" and "public", 
       i.g "if you provide 'top-companies/pulbic/' all the top companies will be provide" i.g "if you provide 'top-companies/private/' 
       you will be provided with only those companies that user have created.
   h. 'delete-company/<slug>/' delete method to delete the comapny, access token required.
   i. 'add-company' use this endpoint to add new company.


For email to work, you will need to setup .env files with this info:

EMAIL_HOST = 'your email host (get it from your email service provider)'
EMAIL_USE_TLS = 
EMAIL_PORT = 
EMAIL_USE_SSL = 
EMAIL_HOST_USER = Youremail@mail.com
EMAIL_HOST_PASSWORD = your email account password.

* pip install -r requirements.txt to install all the required dependency.

* s3 store for hosting static files.