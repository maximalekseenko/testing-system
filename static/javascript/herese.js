let i0_btn = document.getElementById('i0_btn')
let i0_val = document.getElementById('i0_val')
let i1_btn = document.getElementById('i1_btn')
let i1_val = document.getElementById('i1_val')
i0_btn.addEventListener('click', function() {
    i1_val.value = parseInt(i1_val.value) + 3
    i2_val.value = parseInt(i2_val.value) - 4
})
i1_btn.addEventListener('click', function(){
    i0_val.value = parseInt(i0_val.value) - 5
    i2_val.value = parseInt(i2_val.value) + 7
})
i2_btn.addEventListener('click', function(){
    i0_val.value = parseInt(i0_val.value) + 6
    i1_val.value = parseInt(i1_val.value) - 2
})  
