const axios = require("axios")
const cheerio = require("cheerio");
const fs = require("fs");

const uespBaseUrl = "https://en.uesp.net"
const uespPeopleLink = "https://en.uesp.net/wiki/Skyrim:People"
const uespPeopleSelector = "#mw-content-text>* a:not(.mw-headline>a):not(.mw-editsection>a):not(th>a):not(#toc>* a):not(td:nth-child(2)>a):not(sup>a):not(p>a):not(.citation>* a):not(.citation>a):not(i>a):not(#mw-content-text > div > div:nth-child(4)>* a)";


axios.get(uespPeopleLink).then(res => {
    const $ = cheerio.load(res.data);
    const dump = $(uespPeopleSelector).map(function (index, element) {
        const ele = $(this);
        let name = ele.text();
        let link = ele.attr("href");
        if (!link.startsWith("http")) link = new URL(ele.attr("href"), uespBaseUrl).href;
        if (name != "")
            return {
                name: name,
                link: link
            }
    }).toArray();

    fs.writeFile("./SkyrimCharacters.json", JSON.stringify(dump), function (err) {
        if (err)
            console.log(err);
    });
});

