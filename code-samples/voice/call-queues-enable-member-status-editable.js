const RingCentral = require('@ringcentral/sdk').SDK

var rcsdk = new RingCentral({ server: "server_url", clientId: "client_id", clientSecret: "client_secret" });
var platform = rcsdk.platform();

platform.login({ username: "username", password: "password", extension: "extension_number" })

platform.on(platform.events.loginSuccess, async function(response) {
  get_call_queues()
});

async function get_call_queues() {
  try {
    var resp = await platform.get('/restapi/v1.0/account/~/call-queues')
    var jsonObj = await resp.json()
    for (var group of jsonObj.records) {
      get_call_queue_config(record.id)
    }
  } catch (e) {
    console.log(e.message)
  }
}

async function get_call_queue_config(id){
  try{
    var resp = await platform.get(`/restapi/v1.0/account/~/call-queues/${id}`)
    var jsonObj = await resp.json()
    if (jsonObj.editableMemberStatus == false)
      enable_call_queue_editable(jsonObj.id)
  }catch(e){
    console.log(e.message)
  }
}

async function enable_call_queue_editable(id){
  try{
    var params = {
      editableMemberStatus: true
    }
    var resp = await platform.put(`/restapi/v1.0/account/~/call-queues/${id}`, params)
    var jsonObj = await resp.json()
  }catch(e){
    console.log(e.message)
  }
}
