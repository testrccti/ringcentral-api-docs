# Interactive messaging events for Team Messaging

Unlike other outbound events sent by RingCentral, events related to interactive messages do not require the application to explicitly subscribe for a particular set of events. Instead, you will provide an "Outbound webhook URL" when you create your application, to which RingCentral will automatically deliver any event relating to an interactive message posted by that app. 

Interactive messaging events are also unique in that applications are expected to issue a response upon receiving an event that will signal to RingCentral how the system should respond to the event. See "Responding to interactive message events" below. 

## What interactive messaging events are supported?

Currently, the only event RingCentral will transmit to your app is one relating to a user submitting a form contained by a message posted by the corresponding app. 

* See [Adaptive Cards](../../adaptive-cards/)
* See [Creating an Add-in](../../add-ins/creation/)

## Responding to interactive message events

Upon receiving an interactive messaging event, applications should respond with an HTTP status code of 200 in order to acknowledge receipt of the event. A developer should respond this way even if an error occurred while processing the event. If a developer includes a payload in their response, then RingCentral will assume an error occurred, and will look to the payload to determine what message should be displayed to the user. 

If an app responds with any other HTTP status code other than 200, the body of the response (typically a simple plain text string) will be displayed to the user in the client, and the entire transaction will be considered a failure. 

If an app fails to acknowledge receipt within five seconds of an interactive messaging event, RingCentral will interpret that delivery a failure. RingCentral will *not* attempt any redelivery of an event. 

### Response schema

The structure of a response should conform to the following schema:

| Attribute | Required? | Type | Description |
|-|-|-|-|
| `type` | false | enum | The type of response. Allowable values are:  "message". |
| `text` | false | string | The text of the response message. | 

**Example response**

```json
{
   type: 'message',
   text: 'An error occurred. Please display this message to the end user.'
}
```

<!--
**Example error as seen within the client**

!!! danger "TODO - insert a screenshot of what an error message will look like"
-->

## Verifying the authenticity of an event

With every message posted to an Outbound Webhook URL, RingCentral will also transmit an HTTP header called `X-Glip-Signature`. The value of this header will be in the format of:

    sha1=<signature>
	
The signature is generated by computing the HMAC SHA1 hash of the receiving application's "shared secret" (generated for you when you created the app), and the event's payload, or the HTTP post's body.

You can verify that RingCentral is the sender of an event by generating your own signature, and comparing it to the one contained in the HTTP header. 

```js
{!> code-samples/team-messaging/verify-event.js !}
```

### Handling long-running or asynchronous processes

Some actions that a user intiates may produce the need to update the contents of the original message. Consider for example that a message is delivered to a software engineering team about a new software defect. One of the team members clicks a button to "claim" the issue - signaling to the rest of the team that they will fix the issue. When the message is first posted it shows the assignee as "Unassigned." After the user clicks the "Claim" button, the app wants to update the content of the message to show that the assignee is now "Chewbacca."

To accomplish this, use the Team Messaging REST API to fetch the contents of the corresponding post. This is done via the [Get Post](https://developers.ringcentral.com/api-reference/Posts/readGlipPost) endpoint. Then use the [Update Post](https://developers.ringcentral.com/api-reference/Posts/patchGlipPost) endpoint to modify the contents of the post/message. 

## Event schema

Each event transmitted to an outbound webhook URL will contain the following information:

* The app ID associated with the event. 
* The user who triggered the event.
* The chat in which the event was triggered.
* The message or post the event is associated with. 
* The payload of the event, e.g. data submitted by an end user

The payload of the event will contain the data submitted by the user in the form of a name/value pair map.

**Example event**

```js
{
    'uuid': 'abcdefg',
    'timestamp': '2016-03-10T18:07:52.534Z',
    'type': 'button_submit',
    'appId': 'abcdefg-123443-ghijklmnop',
    'user': {
        'id': 'abcdefg-1234',
		'firstName': 'Luke',
		'lastName': 'Skywalker',
		'accountId': '09283928373'
    },
	'conversation': {
        'id': 'abcdefg-1234',
        'type': 'group',
        'public': true,
        'name': 'Going-away party for Han'
	},
	'post': {
        'id': 'abcdefg-1234',
        'creationTime': '2016-03-10T18:07:52.534Z',
        'lastModifiedTime': '2016-03-10T18:07:52.534Z',
	},
	'data': {
	    'foo1' : 'bar1',
	    'foo2' : 'bar2'
	}
}
```

| Attribute | Required? | Type | Description |
|-|-|-|-|
| `uuid` | true | string | UUID of this request |
| `timestamp` | true | datetime | Datetime of sending a notification in ISO 8601 format including timezone, for example 2016-03-10T18:07:52.534Z |
| `type` | true | enum (string) | <"button_submit"> |
| `appId` | false | string | In-App integration identifier |
| `user` | true | object | User who took this action. See user section below. |
| `conversation` | true | object | Conversation where this event happened. See conversation section below | 
| `post` | false | object	| Post for which this interaction is for. See post section below
| `data` | true | object<string,string> | Event payload ( flat Map with string key-value pairs)

### User 

| Attribute | Required? | Type | Description |
|-|-|-|-|
| `id` | true | number | id of the user |
| `firstName` | true | string | first name of the user |
| `lastName` | true | string | last name of the user |
| `accountId` | true | string | RC account id of the user |

### Conversation 

| Attribute | Required? | Type | Description |
|-|-|-|-|
| `id` | true | string | id of the conversation |
| `type` | true | enum(string) | <DM, GROUP, TEAM> |
| `public` | true | boolean | whether conversation is public or not |
| `name` | true | string | name of the conversation |

### Post

| Attribute | Required? | Type | Description |
|-|-|-|-|
| `id` | true | string | id of the post |
| `creationTime` | true | date | ISO 8601 format including timezone, for example 2016-03-10T18:07:52.534Z |
| `lastModifiedTime` | true | date | ISO 8601 format including timezone, for example 2016-03-10T18:07:52.534Z |

