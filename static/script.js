const panels=document.querySelectorAll('.panel');
const plots=["../static/plot0.jpg","../static/plot1.jpg","../static/plot2.jpg","../static/plot3.jpg"];
const background=["https://media.istockphoto.com/photos/an-employee-pulls-a-trolley-for-cleaning-offices-woman-cleaner-is-in-picture-id1316473356?b=1&k=20&m=1316473356&s=170667a&w=0&h=7nYl9IEj2K_MsU4Z0BMVRmhGygh9Nx6vkpVDIvGGHMA=","https://images.unsplash.com/photo-1517646287270-a5a9ca602e5c?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTJ8fHRhcCUyMHdhdGVyfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
,"https://media.istockphoto.com/photos/power-saving-concept-asia-man-changing-compactfluorescent-bulbs-with-picture-id1061085528?b=1&k=20&m=1061085528&s=170667a&w=0&h=W99K7HV2vPUEO7scjS0gADMLhrZ9Jf958zmZcLRXsVw=","https://media.istockphoto.com/photos/bad-smell-or-odor-from-air-conditioner-picture-id1250690129?b=1&k=20&m=1250690129&s=170667a&w=0&h=FAhJ3yvjpZyKTxrskGkUsLUZ9GtpTAYTsfVfGSPhM1o="];
const reqbtn=document.getElementById('button2');
const btn=document.getElementById("button1");
const wholeres=document.getElementById("resall");
const tabarea=document.getElementById('table');
function gettabledata(){
    abc=tabarea.innerText;
    tabarea.innerHTML=abc;
}
const showtable = ()=>{
    
    removeActiveClass();
    wholeres.classList.remove('images');
    btn.textContent='Show All';
    tabarea.classList.toggle('show');

}
window.onload=gettabledata();

panels.forEach((panel,index)=>{
    panel.addEventListener('click',()=>{
        removeActiveClass();
        
        panel.classList.add('active');
        panel.style.cssText=`background-image:url('${plots[index]}');`;
        
    })
})


function removeActiveClass(){
    panels.forEach((panel,index)=>{
        panel.classList.remove('active');
        panel.style.cssText=`background-image:url('${background[index]}');`;
    })
}

btn.addEventListener('click',()=>{
    removeActiveClass();
    tabarea.classList.remove('show');
    wholeres.classList.contains('images')?wholeres.classList.remove('images'):wholeres.classList.add('images');
    wholeres.classList.contains('images')?btn.textContent='Hide':btn.textContent='Show All';
})


reqbtn.addEventListener('click',showtable);

