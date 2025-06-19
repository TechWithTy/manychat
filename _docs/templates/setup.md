
How to generate a token for the Manychat API and where to get parameters
Search

    On this page
        What is API Key?
        How to generate and authorize API Key
        Where can I get parameters (like tag ID)?
        Is there any limit to the number of API calls?

This article explains how to generate a token for the Manychat API and where to get parameters. The following questions will be covered:

    What is API Key?
    How to generate and authorize your token
    Where can I get parameters (like tag ID)?
    Is there any limit to the number of API calls?

The URL to the website listing all the API commands can be found here.

 
What is API Key? 

API Key is a code used to identify the user, developer, or calling program for a website. Manychat provides API Key (PRO feature) to use with the Account Public API. Public API Key can be found in Settings → API.

There is also a Profile Public API that's used for connection to non-bot-specific things like Templates. It requires a different key that can be found here.

 
How to generate and authorize API Key

To use the Manychat API, you need to generate an API Key. Navigate to Settings → API and click Generate your API Key button.

 

⚠️ Note: Refreshing and deleting your token will disable all connected API methods.

 

After a successful token generation, you can use our Swagger to experiment with API. It is available here. 

 

To add your token to Swagger, click the Authorize button:

 

To authorize your token, paste your API Key as a Bearer value and click Authorize:

 

You also can regenerate or delete your API Key in the Settings tab. 

 
Where can I get parameters (like tag ID)?

Contact ID can be found in a contact card in Contacts:

 

Flow_ns can be found in your Automation URL in the address bar:

 

Tag ID – use /fb/page/getTags API method to get a list of all Tag IDs. You can also find it in the interface by proceeding to Settings → Tags and hovering the cursor over the desired tag.

 

Custom User Field ID – use /fb/page/getCustomFields API method to get a list of all User Field IDs. You can also find it in the interface by proceeding to Settings → Fields → User Fields and hovering the cursor over the desired user field.

 
Is there any limit to the number of API calls?

Yes, Manychat has a request-based limit. Refer to the table below for details. When you reach the limits, Manychat may stop processing requests for 24 hours.

PAGE

/fb/page/getInfo

/fb/page/getTags

fb/page/getGrowthTools 

/fb/page/getCustomFields 

/fb/page/getOtnTopics

/fb/page/getBotFields 
	100RPS

PAGE

/fb/page/getFlows
	10RPS

PAGE

/fb/page/createTag

/fb/page/removeTag

/fb/page/removeTagByName

/fb/page/createCustomField

/fb/page/createBotField

/fb/page/setBotField

/fb/page/setBotFieldByName

/fb/page/setBotFields
	10RPS

SENDING

/fb/sending/sendContent

/fb/sending/sendContentByUserRef

/fb/sending/sendFlow
	25RPS

SUBSCRIBER

/fb/subscriber/getInfo

/fb/subscriber/findByName

/fb/subscriber/findByCustomField
	10RPS

SUBSCRIBER

/fb/subscriber/findBySystemField
	100RPS

SUBSCRIBER

/fb/subscriber/addTag

/fb/subscriber/addTagByName

/fb/subscriber/removeTag

/fb/subscriber/removeTagByName

/fb/subscriber/setCustomField

/fb/subscriber/setCustomFields

/fb/subscriber/setCustomFieldByName

/fb/subscriber/verifyBySignedRequest

/fb/subscriber/createSubscriber

/fb/subscriber/updateSubscriber
	10RPS
 
Was this article helpful?
