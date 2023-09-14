
let unej_logo;
let router_on;
let wifi_on;
let router_off;
let wifi_off;
let warning_status = false
let mute = false
let url_audio;

//Fungsi display list device
function display_devices(data){
  let devices = ''
  for(let i=0;i<data.devices.length;i++){
    devices += `<p> ${data.devices[i].device_name}(${data.devices[i].device_ip}) : <b>${data.devices[i].device_status}</b> </p>` 
  } 
  return devices
}


//Get Location URL
$(function(){
    unej_logo = $('#unej-logo').val()  
    url_audio = $('#warning').val()

    $('#btn-mute').on('click', function(){
      mute = true
      $('#btn-unmute').attr('hidden',false)
      $(this).attr('hidden',true)
    })

    $('#btn-unmute').on('click', function(){
      mute = false
      $('#btn-mute').attr('hidden',false)
      $(this).attr('hidden',true)
    })

 
})

let map;

async function initMap() {
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps"); 

  map = new Map(document.getElementById("map"), {
    mapId: "68406db2711b3df8",
    center: { lat: -8.168684, lng: 113.715874 },
    zoom: 19,
  });


  //Get NetMaps Data Nodes
  $.ajax({
    type:'GET',
    url:'get_netmaps_data',
    success: function(response){
      console.log('Success Get Data Netmaps')
      console.log(response)

      data = response

      const iconBase = "https://localhost:8000/static/assets/img/";
      const icons = {
        AP_on: {
          icon: iconBase + "AP-on.png",
        },
        AP_off: {
          icon: iconBase + "AP-off.png",
        },
      };

      let markers =[
            [
          "Universitas Jember",
          -8.164743199040513,
          113.71527408052923,
          unej_logo,
          40,
          40,
          "Universitas Jember"
        ],
      ]

      
      for(let i=0;i<data.devices.length;i++){
        markers.push([

          '<div id="content">' +
          `<div id="siteNotice">${data.devices[i].device_name}` +
          "</div>" +
          `<h1 id="firstHeading" class="firstHeading">${data.devices[i].type}</h1>` +
          '<div id="bodyContent">' +
          ``+
          "</div>" +
          "</div>",

          data.devices[i].lat,

          data.devices[i].long,

          icons[String(data.devices[i].icon)].icon,

          25,

          25,

          data.devices[i].device_name,

        ])

        if(data.devices[i].device_status=='off'){
          console.log('Warning Status to True')
          warning_status=true
        }
        
      }

      for(let i = 0; i<markers.length; i++){
        
        const currentMarker = markers[i];    
        const statusTag = document.createElement("div");

        const beachFlagImg = document.createElement("img");

        beachFlagImg.src = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
        statusTag.className = "test";


          const marker = new google.maps.Marker({
            position: {lat: currentMarker[1], lng: currentMarker[2]},
            map,
            icon: currentMarker[3],
            title: currentMarker[7],
          });

          const infowindow = new google.maps.InfoWindow({
            content: currentMarker[0]
          });

          marker.addListener("click", () => {
            infowindow.open({
              anchor: marker,
              map,
            });
          });

      }

    },
    error: function(response){
      console.log('ERROR')
      console.log(response)
    }
  })
}


function play_warning(){
  $(function(){
    let warning = new Audio($('#warning').val());
    if (!mute){
      if (warning_status){
        warning.play()
        console.log('Warning = True') 
    }else{
      console.log('Warning = False') 
    }
    }else{
      console.log('Mute = True') 
    }
  })
}

initMap()
play_warning()  

setInterval(() => {
initMap()
play_warning()
}, 60000);

