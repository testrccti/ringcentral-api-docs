from ringcentral import SDK
import time, urllib2

sdk = SDK( "client_id", "client_secret", "server_url" )
platform = sdk.platform()
platform.login( "username", "extension", "password" )

def create_compliance_export_task():
    print ("Create export task.")
    endpoint = "/restapi/v1.0/glip/data-export"
    params = {
	"timeFrom": "2019-07-01T00:00:00.000Z",
	"timeTo": "2019-07-29T23:59:59.999Z"
      }
    resp = platform.post(endpoint, params)
    json = resp.json()
    get_compliance_export_task(json.id)

def get_compliance_export_task(taskId):
    print("Check export task status ...")
    endpoint = "/restapi/v1.0/glip/data-export/" + taskId
    response = platform.get(endpoint)
    jsonObj = response.json()
    if jsonObj.status == "Completed":
        length = len(jsonObj.datasets)
        for i in range(length):
            fileName = "rc-export-reports_" + jsonObj.creationTime + "_" + str(i) + ".zip"
            get_report_archived_content(jsonObj.datasets[i].uri, fileName)
    elif jsonObj.status == "Accepted" or jsonObj.status == "InProgress":
        time.sleep(5)
        get_compliance_export_task(taskId)
    else:
      print (jsonObj.status)

def get_report_archived_content(contentUri, zipFile):
    print("Save export zip file to the local machine.")
    uri = platform.create_url(contentUri, False, None, True);
    fileHandler = urllib2.urlopen(uri)
    with open(zipFile, 'wb') as output:
        output.write(fileHandler.read())

create_compliance_export_task()
