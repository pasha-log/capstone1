function randomRGB(){
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`
}

// const h1 = document.querySelector('h1');
const h1 = $('.letter')

setInterval(function(){
    h1.style.color = randomRGB()
}, 500)

// const letters = document.querySelectorAll('.letter')

// setInterval(function(){
//     for (let letter of letters){
//         letter.style.color = randomRGB();
//     }
// }, 1000)

// function changeColor(el, color) {
//     return new Promise((resolve, reject) => {
//         setTimeout(() => {
//             el.style.color = color;
//             $(el).attr('style', )
//             resolve()
//        }, 1000)
//     })
// }

// const $h1 = $('.letter')

// changeColor($h1, 'red')
// .then(() => changeColor($h1, 'orange'))
// .then(() => changeColor($h1, 'yelow'))
// .then(() => changeColor($h1, 'green'))
// .then(() => changeColor($h1, 'blue'))
// .then(() => changeColor($h1, 'indigo'))
// .then(() => changeColor($h1, 'violet'))