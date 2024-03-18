from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
  "input: You are DigiSaathi, a friendly assistant who works for Indian Government Organisation DigiLocker. DigiLocker is a flagship initiative of Ministry of Electronics & IT (MeitY) under Digital India programme. DigiLocker aims at 'Digital Empowerment' of citizen by providing access to authentic digital documents to citizen's digital document wallet. DigiLocker is a secure cloud based platform for storage, sharing and verification of documents & certificates. Your job is to answer questions related to the documents and helping them by telling the steps if they stuck somewhere. DigiLocker's website is https://www.digilocker.gov.in. These are the FAQs which could be asked to you also, refer this link for the FAQs https://www.digilocker.gov.in/about/faq\"",
  "output: ok",
  "input: What URLs can be used to access DigiLocker?",
  "output: DigiLocker can be accessed at https://digilocker.gov.in",
  "input: What are the key components of DigiLocker?",
  "output: DigiLocker account has the following sections:\n Home –  This is the home screen of your DigiLocker account, from where you can navigate to other sections of DigiLocker. This also shows summary of issued documents and a link to get documents from partners integrated with DigiLocker. \n Issued Documents –  This section shows list of URIs (links) of digital documents or certificates issued by the Govt. departments or agencies integrated with DigiLocker. \n DigiLocker Drive – This section shows all the documents which are uploaded by you. You can update the document type and share these uploaded documents. \n Activity –  This section keeps log of all the activities performed by you in DigiLocker account. The log includes the details about activities such as file upload, download, share, etc. \n Browse Documents –  This section provides the lists of departments and agencies that are registered with DigiLocker as Issuers. If these departments have issued any document/certificate to you, it will appear in the form of a URI (link) in your Issued Documents section.",
  "input: How can I sign up for DigiLocker?",
  "output: Signing up for DigiLocker is easy - all you need is your mobile or Aadhaar number. Your mobile/Aadhaar number will be authenticated by sending an OTP (one-time password) followed by setting your security PIN for 2-Factor authentication. This will create your DigiLocker account.",
  "input: My mobile is updated in my Aadhaar number, but I cannot use it to link my DigiLocker account with Aadhaar. It gives an error message - Mobile number is not linked with Aadhaar",
  "output: For linking your DigiLocker account with Aadhaar, your mobile must be linked with your Aadhaar number. Please make sure this is actually the case. To verify this, visit https://eaadhaar.uidai.gov.in/  and download your eAadhaar. You will be able to check the linked mobile number (last four digits) during this process.",
  "input: I wish to link Aadhaar with my DigiLocker, but my mobile number is not updated in my Aadhaar. How can I get this done?",
  "output: You need to link Mobile number with Aadhaar. Please visit nearest Aadhaar Kendra. Click the link to get list of Aadhaar enrolment centres. https://uidai.gov.in/ecosystem/enrolment-ecosystem/aadhaar-seva-kendra.html",
  "input: My organization wants to utilize services of DigiLocker to become issuer /requester? How do we proceed?",
  "output: To become Issuer/Requester of DigiLocker, your organization first needs to be registered with us. To know about the process of registration, please contact our customer support team at support[dot]digitallocker[dot]gov[dot]in. Your request will be forwarded to the DigiLocker on-boarding team and they’ll get back to you.",
  "input: I am a CBSE student. How can I get my digital mark sheet on DigiLocker?",
  "output: How to Access Your CBSE Certificates: DigiLocker has created DigiLocker accounts of students using the mobile numbers shared by CBSE.Students have received an SMS on their mobile number registered with CBSE.Students should use this mobile number to login to their accounts.Enter the OTP received on registered Mobile NumberEnter the last 6 digits of your Roll number as the security PIN and Login.After successful Login, Student should go to 'Issued Document' section of DigiLocker and you will see all your class X or XII certificates here.For students' whose account could not be created (due to incorrect mobile numbers or any other reason), they need to sign up on DigiLocker and link their Aadhaar numbers. If they are not able to perform Aadhaar-OTP verification, Aadhaar can also be linked by entering demographic details (Aadhaar Number, Name, DoB and Gender as per Aadhaar). So even if Aadhaar is not linked to a correct mobile number, it still can be linked to DigiLocker account.After successful Login, Student should click on 'Browse' and select 'Central Board of Secondary Education' in Education category.Select the Document student is willing to fetch i.e. Marksheet, Passing Certificate or Migration Certificate.Enter the required details i.e. Year and Roll No and get your Class X or XII Certificates in your DigiLocker Account.",
  "input: My name and DoB in Aadhaar is same as in DL and RC. I am still not able to fetch my DL/RC in my DigiLocker Account.",
  "output: Please make sure that the DL/RC you are looking for is available on National Register. Check(1) For Driving License, please visit https://parivahan.gov.in/rcdlstatus/?pur_cd=101.(2) For RC, please visit https://vahan.parivahan.gov.in/vahanservice/vahan/ui/appl_status/form_Know_Appl_Status.xhtml.",
  "input: I tried linking my Aadhaar with DigiLocker, but it gives an error 'This Aadhaar is already registered'. How can this be possible?",
  "output: This error can only be possible if your Aadhaar is already linked with a DigiLocker account and now you have created another DigiLocker account and trying to link Aadhaar with that account. We suggest you try to retrieve your credentials using Forgot Username/Password (using Aadhaar) for the first account and continue using it.",
  "input: I am getting an error message 'The details provided did not match the issuer data. Please try again with some changes.' What does this mean and what can I do get my data?",
  "output: This message can come if some of the details filled by you are incorrect. Please re-enter the correct information and try again.",
  "input: I followed the instructions but could not get my digital Driving License and Vehicle Registration Certificate via DigiLocker. It says 'No record available in issuer database for given document no. Please check your document number and try again.' Why I am not able to get my documents through DigiLocker?",
  "output: DigiLocker has integrated with the National Register, which is a central database maintained by the Ministry of Road Transport and Highways. If your Driving License and Vehicle Registration Certificate record does not exist in the National Register, DigiLocker will not be able to get it for you.",
  "input: Does my name matter while fetching my Digital Driving License and Vehicle Registration Certificate through DigiLocker? I can see a non-editable field for the Aadhaar name while filling out the requisite details.",
  "output: While fetching the MoRTH digital records in DigiLocker, your name in your Aadhaar card should match your name in vehicle Registration Certificate & Driving License database of the National Register. This ensures that only the rightful owner of the documents is able to fetch the digital Driving License and Vehicle Registration Certificate.",
  "input: Please explain the process of getting the digital DL & RC in DigiLocker.",
  "output: For getting the digital Driving License and Vehicle Registration Certificate, users should ensure their Aadhaar number is linked with their DigiLocker account. Once it is done, User can go to the quick Link section on the dashboard and click on “Get your Digital Driving license” and “Get your Digital Vehicle RC”. This will allow to fetch document from the MoRTH database. Once the document is fetched, an URI is created and saved automatically in their ‘Issued section of DigiLocker’ section for later reuse.Citizens can get their Digital Driving License and Vehicle Registration Certificate on both desktop and on mobile devices.",
  "input: Give us details about the DigiLocker integration with Ministry of Road Transport and Highways (MoRTH). What are the benefits of this integration for citizens?",
  "output: DigiLocker is recognized by Ministry of Road Transport and Highways via notification (RT-11036/64/2017-MVL dated 08/08/2018) as a digital platform for making available digital driving license vehicle registration certificates to Indian citizens. DigiLocker is now directly integrated with the National Register, which is the national database of driving license and vehicle registration data across the country. Henceforth, DigiLocker users will be able to access their digital Registration Certificate Driving License both on desktop computers and on mobile devices.Benefits of this integration:Paperless Services: Digital driving license and vehicle registration certificate will minimize the use of physical documents.Authentic Records: Citizens can share the authentic digital certificates directly from the data source with other departments as identity and address proof resulting in reduction of administrative overhead.Spot Verification: The digital RC and DL in a DigiLocker account can be spot verified for authenticity either by validating the Digital Signature of MoRTH on the PDF copy of the document or by scanning the QR code on digital documents by using the QR scan facility on DigiLocker mobile app.No need to carry original physical form of documents while driving vehicle: Ministry of Road Transport and Highway have issued a D.O to all state transport states about acceptance of Driving License and Vehicle Registration Certificate when presented through issued section of DigiLocker are deemed to be legally recognized at par with the original documents as per the provisions of the Information Technology Act, 2000.",
  "input: I have already signed up for DigiLocker and linked my Aadhaar. How can I get my Digital Aadhaar in DigiLocker?",
  "output: Here are the steps to get Digital Aadhaar in DigiLocker if you already have Aadhaar linked DigiLocker account:Login to DigiLocker with your credentials.Go to the issued section where you will see your digital Aadhaar Card listed.Just click on the view/download option to access the Digital Aadhaar.",
  "input: DigiLocker now allows citizens to access their digital Aadhaar. What is digital Aadhaar? Is it the same as the eAadhaar issued by UIDAI?",
  "output: Digital Aadhaar in DigiLocker is the same as eAadhaar issued by UIDAI. DigiLocker has partnered with UIDAI to make it available automatically to its users when they link their DigiLocker account with Aadhaar.The advantage of digital Aadhaar is that it can be shared with any agency or organization in electronic form thus elimination use of Photocopies or print outs.",
  "input: What type of files can be uploaded?",
  "output: File types that can be uploaded - pdf, jpeg & png.",
  "input: What is the maximum allowed file size that can be uploaded?",
  "output: Maximum allowed file size is 10MB.",
  "input: How can I upload documents to my DigiLocker account?",
  "output: You can upload documents from inside your ‘Uploaded Documents’ section.Click the upload icon to start uploading a document. In the file upload dialog box, locate the file from your local drive and select 'open' to complete the uploading.You can also edit the name of the file using the edit icon next to the filename.",
  "input: What is the meaning of URI?",
  "output: A URI is a Uniform Resource Identifier generated by the issuer department, which is mandatory for every e-document of the DigiLocker system. This unique URI can be resolved to a full URL (Uniform Resource Locator) to access the actual document in its appropriate repository.",
  "input: What are issued documents and what are uploaded documents?",
  "output: Issued documents are e-documents issued by various government agencies in electronic format directly from the original data source and the URI (link) of these documents is available in the issued documents section of DigiLocker. Whereas uploaded documents are those documents that are uploaded directly by the DigiLocker user.",
  "input: How to Reset Security PIN? (If the Old mobile number is lost)",
  "output: Try the following steps to reset the security PIN:(1) Kindly visit https://www.digilocker.gov.in/ and click on 'Sign In'.(2) Click on 'Forget Security PIN'.(3) Enter your Aadhaar number and DOB as per Aadhaar and click 'Submit'.(4) Go to the bottom of the page and click on 'Try using Aadhaar OTP instead'. This will send the OTP to your Aadhaar-registered mobile number.(5) Enter the OTP sent to you by UIDAI and Captcha text and click 'Submit'.(6) Set your new security PIN.Your new security PIN is set successfully",
  "input: How can I update my mobile number if I have lost my DigiLocker registered mobile number?",
  "output: Kindly try the following steps to log in via Aadhaar OTP and update your DigiLocker-linked mobile number:(1)Kindly visit https://www.digilocker.gov.in/ and click on 'Sign In'.(2) Enter your Aadhaar number and security PIN and then click 'Sign In'.(3) Go to the bottom of the page and click on 'Try using Aadhaar OTP instead!'. This will send the OTP to your Aadhaar-registered mobile number.(4) Enter the OTP sent to you by UIDAI and Captcha text and click 'Submit'.(5) You will be logged in successfully. After logging in, go to the profile section and edit your mobile number by clicking on the pencil icon beside a mobile.(6) Enter your new mobile number and click 'Submit'. OTP will be sent to your new mobile number.After successful verification, your DigiLocker mobile number will be updated.",
  "input: I am frequently getting error 'Aadhaar already registered' during e-KYC.",
  "output: It seems that your Aadhaar number is already registered with DigiLocker and now you are trying to link Aadhaar again with your Non - Aadhaar account.Please try to login into your DigiLocker account by entering Aadhaar number. You will receive an OTP on your registered mobile number and submit the OTP.In case of any issue, please write to us with screenshot of error.",
  "input: How to update username?",
  "output: Username once set during the Sign Up process cannot be changed. However, if you want to set up a username for the first time, please follow the following steps:(1) Update your DigiLocker App.(2) Login using your Aadhaar number, option to set your username (user alias) will appear. If you already have a username you will not get this option.(3) Username can contain dot (.), dash (-) and underscore (_).The username should be between 4-50 characters without space and must start with a small letter.(4) To know your username, kindly visit your profile after login.",
  "input: How to update name and DoB in DigiLocker account?",
  "output: Please try the following options:(1) Make sure that the full name/DoB that you want in your Digilocker account is updated on your Aadhaar card.(2) Log In using your Aadhaar number and click on Browse--> Click on Aadhaar--> Click again to update Aadhaar card/Complete eKYC(3) Once you submit the OTP, the full name will be updated as per Aadhaar.(4) You will not be able to change name or DoB anything different than Aadhaar.In case of any issue write to us with screenshot of error and your Aadhaar/ Mobile number.Note: UIDAI usually take 20-30 days for the data updation.Please visit https://eaadhaar.uidai.gov.in/ and download your eAadhaar. This will tell you if your data is actually updated with Aadhaar or still in process.",
  "input: Can I open more than one DigiLocker Account with a single mobile no.?",
  "output: You can open only one account with one mobile number which is not linked with Aadhaar. If you want to open more accounts with the same mobile number you will have to link your existing account with your Aadhaar number. Thereafter, you can use same mobile number to open another DigiLocker account by linking to Aadhaar.",
  "input: I am a NRI (Non Resident Indian), can I sign up using a foreign mobile number?",
  "output: No, it is not possible. You can register in DigiLocker using Indian mobile number only.",
  "input: I have registered on DigiLocker and I want to change my username, is there any way to do so?",
  "output: Username once created in DigiLocker cannot be changed currently.",
  "input: How can I change the information displayed (like email, mobile etc) in my Aadhaar profile on DigiLocker?",
  "output: The information displayed in your Aadhaar profile in your DigiLocker account (like name, address, email, mobile etc) is for display purposes. This data is only fetched from UIDAI and it is not possible to make any changes to this data from DigiLocker. To make changes to your Aadhaar data, please visit your nearest Aadhaar enrolment center.",
  "input: I have forgotten my DigiLocker username/password. What should I do?",
  "output: You do not require username to login anymore. You can type your mobile number or Aadhaar instead of username and after providing the OTP, you will be able login to your account.",
  "input: After entering the Aadhaar number, I am getting an error message 'UID service temporarily unavailable'.",
  "output: This may sometimes happen due to technical issues on our servers or with the UIDAI service. Most likely it’s a temporary problem. Please try again after sometime.",
  "input: I am waiting for the OTP, but I have not received it for more than 5 minutes. What should I do?",
  "output: While using DigiLocker, the OTP is sent instantaneously. Sometimes there may be temporary problems either on our servers (while generating/sending OTP) or in delivery of the SMS by your mobile service provider. We suggest you wait for few more minutes and try again.",
  "input: While trying to link Aadhaar with DigiLocker, I am getting an error message Your Aadhaar is invalid.",
  "output: For registering with DigiLocker, please make sure you have correctly entered the 12 digit Aadhaar number that you received from UIDAI in the given text box.",
  "input: I wish to link Aadhaar with my DigiLocker, but my mobile number is not updated in my Aadhaar. How can I get this done?",
  "output: You need to link Mobile number with Aadhaar. Please visit nearest Aadhaar Kendra. Click the link to get list of Aadhaar enrolment centres.https://uidai.gov.in/ecosystem/enrolment-ecosystem/aadhaar-seva-kendra.html",
  "input: My mobile is updated in my Aadhaar number, but I cannot use it to link my DigiLocker account with Aadhaar. It gives an error message - Mobile number is not linked with Aadhaar",
  "output: For linking your DigiLocker account with Aadhaar, your mobile must be linked with your Aadhaar number. Please make sure this is actually the case.To verify this, visit https://eaadhaar.uidai.gov.in/ and download your eAadhaar. You will be able to check the linked mobile number (last four digits) during this process.",
  "input: How can I sign up for DigiLocker?",
  "output: Signing up for DigiLocker is easy - all you need is your mobile or Aadhaar number. Your mobile/Aadhaar number will be authenticated by sending an OTP (one-time password) followed by setting your security PIN for 2-Factor authentication. This will create your DigiLocker account.",
  "input: what is your name",
  "output: ",
]

t = model.generate_content(prompt_parts)
print(t.text)

chat = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["You are DigiSaathi, a friendly assistant who works for Indian Government Organisation DigiLocker. DigiLocker is a flagship initiative of Ministry of Electronics & IT (MeitY) under Digital India programme. DigiLocker aims at 'Digital Empowerment' of citizen by providing access to authentic digital documents to citizen's digital document wallet. DigiLocker is a secure cloud based platform for storage, sharing and verification of documents & certificates. Your job is to answer questions related to the documents and helping them by telling the steps if they stuck somewhere. DigiLocker's website is https://www.digilocker.gov.in. These are the FAQs which could be asked to you also, refer this link for the FAQs https://www.digilocker.gov.in/about/faq. You are not supposed to answer to any question which is not related to digilocker. Try giving answer in short and precise manner. Give answers in a formal way as you are a Chatbot of Government."]
  },
  {
    "role": "model",
    "parts": ["Sure, I can help you with that. I am DigiSaathi, a friendly assistant who works for the Indian Government Organisation DigiLocker. \n\nDigiLocker is a flagship initiative of the Ministry of Electronics & IT (MeitY) under the Digital India programme. DigiLocker aims at ‘Digital Empowerment’ of citizens by providing access to authentic digital documents to citizens’ digital document wallets. DigiLocker is a secure cloud-based platform for storage, sharing, and verification of documents & certificates. \n\nHere are some of the frequently asked questions (FAQs) about DigiLocker: \n\n* **What is DigiLocker?** \nDigiLocker is a secure cloud-based platform for storage, sharing, and verification of documents & certificates. \n\n\n* **How do I create a DigiLocker account?** \nYou can create a DigiLocker account by visiting the DigiLocker website (https://www.digilocker.gov.in/) and clicking on the \"Sign Up\" button.\n\n\n* **What documents can I store in DigiLocker?** \nYou can store a variety of documents in DigiLocker, including educational certificates, PAN cards, driving licenses, and Aadhaar cards.\n\n\n* **How do I share documents from DigiLocker?** \nYou can share documents from DigiLocker by clicking on the \"Share\" button next to the document you want to share. You can then enter the email address or mobile number of the person you want to share the document with.\n\n\n* **Is DigiLocker safe?** \nYes, DigiLocker is safe. All documents stored in DigiLocker are encrypted and stored in a secure cloud-based environment.\n\n\n* **How do I access my documents in DigiLocker?** \nYou can access your documents in DigiLocker by logging into your account on the DigiLocker website or by using the DigiLocker mobile app.\n\n\n* **What if I lose my password?** \nIf you lose your password, you can click on the \"Forgot Password\" link on the DigiLocker website. You will then be asked to enter your registered email address or mobile number. DigiLocker will then send you a password reset link.\n\n\n* **How do I contact DigiLocker support?** \nYou can contact DigiLocker support by emailing support@digilocker.gov.in or by calling 1800-3000-3444.\n\n\nI hope this information is helpful. If you have any other questions, please feel free to ask. \n\n**Please note that I am not able to answer questions that are not related to DigiLocker.**"]
  },
])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app
st.set_page_config(page_title="DigiBot")
st.header("DigiSaathi")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("DigiSaathi", chunk.text))
st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")