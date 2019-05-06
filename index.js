const fs = require('fs')

const getHtml = (body) => {
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
        </head>
        <body>
            <h1>Test Report for last 10 Days:</h1>
            ${body}
        </body>
        </html>
    `
}

const getList = (arr) => {
    return `
        <ul>
            ${arr.map(item => `<li>${item}</li>`).join('\n')}
        <ul>
    `
}
const DAY = 24 * 60 * 60 * 1000
const now = Date.now()

const formatDateString = (str) => {
    if (str.length < 2) {
        return `0${str}`
    }
    return str
}
const getDate = (date) => {
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    return `${year}${formatDateString(String(month))}${formatDateString(String(day))}`
}


const getHtmlFileName = (date) => `${getDate(date)}Report.html`

const arr = []
for (let i = 0; i < 10; i++) {
    const date = new Date(now - i * DAY)
    arr.push(`<a href=${getHtmlFileName(date)}>${getDate(date)}</a>`)
}

const htmlContent = getHtml(getList(arr))
fs.writeFile('report-10days.html', htmlContent, () => {
    console.log('done')
})