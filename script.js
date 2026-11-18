async function sendmessage(){
    let chat = document.getElementById("chat");
    let message = document.getElementById("message").value;
    let box = document.createElement("div");
    box.innerText = "You: " + message;
    chat.appendChild(box);
    document.getElementById("message").value="";
    try{
        let response = await fetch("/chat", {method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({message:message})
        });
        let data = await response.json()
        console.log(data.response)
        let reply = document.createElement("div");
        reply.innerText = "Nova: " + data.response;
        chat.appendChild(reply);
    }
    catch (error){
        console.log("Something went wrong: ",error)
    }
    
}
// Har 3 sec me check karo Sooraj ne jawab diya ya nahi
setInterval(async () => {
    try{
        let res = await fetch("/check_admin_reply");
        let data = await res.json();
        if(data.reply){
            let chat = document.getElementById("chat");
            let reply = document.createElement("div");
            reply.innerText = "Sooraj: " + data.reply;
            chat.appendChild(reply);
        }
    }catch(e){}
}, 3000);

function newchat(){
    document.getElementById("chat").innerHTML = "";
}
function settings(){
    alert("This is under process so please wait for next update. Thank You!!");
}
