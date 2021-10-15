const toggles=document.querySelectorAll('.img-toggle');
const btn=document.getElementById('btn');
const tabarea=document.getElementById('table');
// with out variable
window.onload=gettabledata();
function gettabledata(){
    abc=tabarea.innerText;
    tabarea.innerHTML=abc;
}
toggles.forEach(toggle=>{
    toggle.addEventListener('click',()=>{
        tabarea.classList.remove('show');
        if(toggle.parentNode.classList.contains('active')){
            toggle.parentNode.classList.remove('active');
        }
        else{
       removeClass();
       toggle.parentNode.classList.add('active');
        }
    })
})
function removeClass(){
    toggles.forEach(toggle=>{
        toggle.parentNode.classList.remove('active');
    })
}
btn.addEventListener('click',()=>{
    removeClass();
    if(tabarea.classList.contains('show')){
        tabarea.classList.remove('show');
    }
    else{
        tabarea.classList.add('show');
    }
    
})























