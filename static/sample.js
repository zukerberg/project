const labels=document.querySelectorAll('.form-control label');
const selects=document.querySelectorAll('.form-control select');
const btn=document.querySelector('.btn');
const inputs=document.querySelectorAll('input');
labels.forEach((label)=>{
    label.innerHTML=label.innerText.split('').map((letter,idx)=>`<span style="transition-delay:${idx * 40}ms">${letter}</span>`).join('');


});
inputs.forEach((input,index)=>{
    input.addEventListener('focusin',()=>{
        input.type='date';
        input.style.color="#fff";
        labels[index+3].childNodes.forEach(node=>{
            node.classList.add('active');
        });
    })
})
selects.forEach((select,index)=>{
    select.addEventListener('focusin',()=>{
        labels[index].childNodes.forEach(node=>{
            node.classList.add('active');
        });
    })
})
selects.forEach((select,index)=>{
    select.addEventListener('focusout',()=>{
        labels[index].childNodes.forEach(node=>{
            if(select.value==='None'){
                node.classList.remove('active');
            }
        });
    })
})
inputs.forEach((input,index)=>{
    input.addEventListener('focusout',()=>{
        labels[index+3].childNodes.forEach(node=>{
            if(input.value===''){
                input.type='';
                node.classList.remove('active');
            }
        });
    })
})

btn.addEventListener('click',()=>{
    var frm = document.getElementsByTagName('form')[0];
   frm.submit(); // Submit the form
   frm.reset();  // Reset all form data
   return false; // Prevent page refresh
})

