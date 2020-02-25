document.addEventListener('DOMContentLoaded',()=>{
    var socket = io.connect('http://'+document.domain+":"+location.port);
    // socket.on('connect',()=>
    // {
    //     socket.send("I am connect")
    // })
    //Display incoming messages
    let room;

    socket.on('message',data=>
    {
        console.log(`Message Received: ${data} `)
        
        const p = document.createElement('p')
        const span_username =  document.createElement('span')
        const span_timestamp = document.createElement('span')
        const br =  document.createElement('br')
        span_username.innerHTML = data.username
        console.log(data.time_stamp)
        span_timestamp.innerHTML = data.time_stamp
        p.innerHTML = span_username.outerHTML + br.outerHTML+ data.msg +br.outerHTML+span_timestamp.outerHTML
        document.querySelector('#display-message-section').append(p);

    })
    
    //Send Message
    document.querySelector('#send_message').onclick = ()=>
    {
        socket.send( {'msg':document.querySelector('#user_message').value,
                    'username':username,'room':room 
                    }
    )
    }

    //Room Selection
    document.querySelectorAll('select-room').forEach(p=>
        {
            p.onclick = ()=>{
                let newRoom = p.innerHTML
                if(newRoom==room)
                {
                    msg = `You are already in ${room} room`
                    printSysMsg(msg)
                }
                else
                {
                    leaveRoom(room)
                    joinRoom(newRoom)
                    room = newRoom
                }

            }
        })

    //Leaving Room
    function leaveRoom(room)
    {
        socket.emit('leave',{'username':username,'room':room})
    }
    function joinRoom(room)
    {
        socket.emit('join',{'username':username,'room':room})
        //clear mssg area
        document.querySelector('display-message-section').innerHTML=''

    }
    function printSysMsg(msg)
    {
        
    }




})