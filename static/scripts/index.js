var tickers = JSON.parse(localStorage.getItem('tickers')) || [];
var lastPrices = {};
var counter = 15;
    
const startUpdateCycle = () => {
    updatePrices();
    setInterval(() => {
        counter --;
        if(counter <= 0){
            updatePrices();
            counter = 15;
        }
    }, 1000)
}

$(document).ready(() => {

tickers.forEach((ticker)=>{
    addTickerToGrid(ticker);
})

updatePrices();

$("#add-ticker-form").submit((e)=>{
    e.preventDefault();
    var newTicker = $('#new-ticker').val().toUpperCase();
    if(!tickers.includes(newTicker)){
        tickers.push(newTicker);
        localStorage.setItem('tickers', JSON.stringify(tickers))
        addTickerToGrid(newTicker);
    }
    $('new-ticker').val('');
    updatePrices();
})

$('#tickers-grid').on('click', '.remove-btn', function() {
    console.log(1)
    var tickerToRemove = $(this).data('ticker');
    tickers = tickers.filter(t => t !== tickerToRemove);
    localStorage.setItem('tickers', JSON.stringify(tickers))
    $(`#${tickerToRemove}`).remove();
});
startUpdateCycle();

});

const addTickerToGrid = (ticker) =>{
    $('#tickers-grid').append(`<div id="${ticker}" class="stock-box"><h2>${ticker}</h2>
        <p id="${ticker}-price"></p><p id="${ticker}-pct"></p>
        <button class="remove-btn" data-ticker="${ticker}">Remove</button></div>`)

}
const updatePrices = () => {
    tickers.forEach((ticker)=>{
        $.ajax({
            url: '/watchlist',
            type: "POST",
            data: JSON.stringify({
                'ticker': ticker
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: (data) => {
                var changePercent = ((data.currentPrice-data.openPrice)/ data.openPrice) * 100;
                var colorclass;
                if(changePercent <= -2){
                    colorclass = 'dark-red';
                }
                else if(changePercent < 0){
                    colorclass = 'red';
                }
                else if(changePercent == 0){
                    colorclass = 'gray';
                }
                else if(changePercent <= 2){
                    colorclass = 'green';
                }
                else{
                    colorclass = 'dark-green';
                }

                $(`#${ticker}-price`).text(`$${data.currentPrice.toFixed(2)}`);
                $(`#${ticker}-pct`).text(`${changePercent.toFixed(2)}%`);

                $(`#${ticker}-price`).removeClass(`dark-red red gray green dark-green`).addClass(colorclass);
                $(`#${ticker}-pct`).removeClass(`dark-red red gray green dark-green`).addClass(colorclass);

                var flaskClass;
                if(lastPrices[ticker]>data.currentPrice){
                    flaskClass = 'red-flask';
                }else if(lastPrices[ticker]<data.currentPrice){
                    flaskClass = 'green-flask';
                }
                else{
                    flaskClass = 'gray-flask'
                }
                lastPrices[ticker] = data.currentPrice;

                $(`#${ticker}`).addClass(flaskClass);
                setTimeout(()=>{
                    $(`#${ticker}`).removeClass(flaskClass);
                }, 1000);
            }
        });
    });
}




var chart = LightweightCharts.createChart(document.getElementById('chart-container'), {
    width: document.getElementById('chart-container').clientWidth,
    height: 550
});

var candleSeries = chart.addCandlestickSeries();

chart.applyOptions({
    timeScale: {
        timeVisible:true,
        secondsVisible:true
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    }
//<!-- --- - -  Live Comment Code- - - - - - --  - - - - -- - - - - - -- - - - - - - -- - - - -  -   -->


//append new comments 
});

var btc = document.getElementById("bitcoin");
var ltc = document.getElementById("litecoin");
var eth = document.getElementById("ethereum");
var doge = document.getElementById("dogecoin");

var liveprice = {
    "async": true,
    "scroosDomain": true,
    "url": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Clitecoin%2Cethereum%2Cdogecoin&vs_currencies=usd",

    "method": "GET",
    "headers": {}
}

$.ajax(liveprice).done(function (response){
    console.log(response)
    btc.innerHTML = response.bitcoin.usd;
    ltc.innerHTML = response.litecoin.usd;
    eth.innerHTML = response.ethereum.usd;
    doge.innerHTML = response.dogecoin.usd;

});
fetch('/data')
    .then(response => response.json())
    .then(data => {
        
        const formattedData = data.map(item => ({
            time: ((new Date(item.date).getTime() / 1000) - (5 * 60 * 60)), // Convert UTC to EST (Standard Time)
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
            volume: item.volume
        }));

        candleSeries.setData(formattedData);
        //console.log((new Date(item.date).getTime() / 1000))
    })
    .catch(error => console.error('Error fetching data:', error));

    
    
var socket = io.connect();
socket.on('updateSensorData', (new_value)=>{
    data = JSON.parse(new_value['value']);

    const updatedData = {
        time: ((new Date(data.date['0']).getTime() / 1000) - (5 * 60 * 60)),
        open: data.open['0'],
        high: data.high['0'],
        low: data.low['0'],
        close: data.close['0']
    };
    console.log(updatedData);
    candleSeries.update(updatedData);

    
});

$('#sendBtn').on('click', function(){
    socket.send($('#comment-input').val());
    $('#comment-input').val('');
});

socket.on("message", (data)=>{
    $("#comments-container").append($("<div>").html(`<strong>${data.username}:</strong>${data.content}`));
});

socket.on('redirect', function(data) {
    window.location.href = data.url; // Redirect to the specified URL
});

fetch('/comment')
.then(response => {
    if (response.ok) {
        return response.json();
    } else {
        throw new Error(`Error: ${response.status}`);
    }
})
.then(comments => {
    document.getElementById("comments-container").innerHTML = '';
    comments.forEach(comment => {
        let commentElement = document.createElement("div");
        commentElement.innerHTML = `<strong>${comment.username}:</strong> ${comment.content}`;
        document.getElementById("comments-container").appendChild(commentElement);
    });
})
.catch(error => {
    console.error('Error fetching comments:', error);
});



// socket.on('new_comment', function(commentData) {   
//     let commentElement = document.createElement("div"); 
//     commentElement.innerHTML = `<strong>${commentData['username']}:</strong> ${commentData['content']}`; 
//     document.getElementById("comments-container").appendChild(commentElement); 
// });

// function submitComment() { 
//     let commentContent =document.getElementById("comment-input").value; 
//     socket.emit('send_comment', { comment: commentContent}); 
//     document.getElementById("comment-input").value = ' '; 
// } 


    // getting all required elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");
let webLink;

// if user press any key and release
inputBox.onkeyup = (e)=>{
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if(userData){
        icon.onclick = ()=>{
            webLink = `https://www.google.com/search?q=${userData}`;
            linkTag.setAttribute("href", webLink);
            linkTag.click();
        }
        emptyArray = suggestions.filter((data)=>{
            //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data)=>{
            // passing return data inside li tag
            return data = `<li>${data}</li>`;
        });
        searchWrapper.classList.add("active"); //show autocomplete box
        showSuggestions(emptyArray);
        let allList = suggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "select(this)");
        }
    }else{
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
}

function select(element){
    let selectData = element.textContent;
    inputBox.value = selectData;
    var regExp = /\(([^)]+)\)/;
            var stock_ticker = regExp.exec(inputBox.value);
            fetch('/data', {
                headers : {
                    'Content-Type' : 'application/json'
                },
                method : 'POST', 
                body : JSON.stringify( {
                    Stock : stock_ticker[1]
                })
            })                
            .then(response => response.json())
            .then(data => {
                
                const formattedData = data.map(item => ({
                    time: ((new Date(item.date).getTime() / 1000) - (5 * 60 * 60)), // Convert UTC to EST (Standard Time)
                    open: item.open,
                    high: item.high,
                    low: item.low,
                    close: item.close,
                    volume: item.volume
                }));

                candleSeries.setData(formattedData);
                //console.log((new Date(item.date).getTime() / 1000))
            })
            .catch(error => console.error('Error fetching data:', error));
    searchWrapper.classList.remove("active");
    console.log(1)
}

function showSuggestions(list){
    let listData;
    if(!list.length){
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
    listData = list.join('');
    }
    suggBox.innerHTML = listData;
}
let suggestions = [
"3M Company (MMM)",
"Abbott Laboratories (ABT)",
"AbbVie Inc. (ABBV)",
"Adobe Inc. (ADBE)",
"Advanced Micro Devices, Inc. (AMD)",
"Alibaba Group Holding Limited (BABA)",
"Alphabet Inc. Class A (GOOGL)",
"Alphabet Inc. Class C (GOOG)",
"Amazon.com, Inc. (AMZN)",
"AMD (Advanced Micro Devices, Inc.)",
"American Express Company (AXP)",
"American International Group, Inc. (AIG)",
"Amgen Inc. (AMGN)",
"Apple Inc. (AAPL)",
"AT&T Inc. (T)",
"Bank of America Corporation (BAC)",
"Berkshire Hathaway Inc. (BRK.B)",
"BlackRock, Inc. (BLK)",
"Boeing Co. (BA)",
"Caterpillar Inc. (CAT)",
"Chevron Corporation (CVX)",
"Cisco Systems, Inc. (CSCO)",
"Citigroup Inc. (C)",
"Coca-Cola Company (KO)",
"Coinbase Global, Inc. (COIN)",
"Comcast Corporation (CMCSA)",
"Costco Wholesale Corporation (COST)",
"CVS Health Corporation (CVS)",
"Delta Air Lines, Inc. (DAL)",
"eBay Inc. (EBAY)",
"Eli Lilly and Company (LLY)",
"Exxon Mobil Corporation (XOM)",
"Facebook, Inc. (FB)",
"FedEx Corporation (FDX)",
"Ford Motor Co. (F)",
"General Electric Company (GE)",
"General Motors Company (GM)",
"Gilead Sciences, Inc. (GILD)",
"Goldman Sachs Group, Inc. (GS)",
"Home Depot, Inc. (HD)",
"International Business Machines Corporation (IBM)",
"Intel Corporation (INTC)",
"Intuit Inc. (INTU)",
"Johnson & Johnson (JNJ)",
"JPMorgan Chase & Co. (JPM)",
"Lockheed Martin Corporation (LMT)",
"Lowe's Companies, Inc. (LOW)",
"Mastercard Incorporated (MA)",
"McDonald's Corporation (MCD)",
"Merck & Co., Inc. (MRK)",
"Meta Platforms Inc. (META)",
"Microsoft Corporation (MSFT)",
"Morgan Stanley (MS)",
"Netflix, Inc. (NFLX)",
"Nike, Inc. (NKE)",
"NIO Inc. (NIO)",
"NVIDIA Corporation (NVDA)",
"Oracle Corporation (ORCL)",
"PayPal Holdings, Inc. (PYPL)",
"Pfizer Inc. (PFE)",
"Procter & Gamble Company (PG)",
"Qualcomm Incorporated (QCOM)",
"Raytheon Technologies Corporation (RTX)",
"Salesforce.com Inc. (CRM)",
"Snap Inc. (SNAP)",
"Sony Group Corporation (SONY)",
"Square, Inc. (SQ)",
"Starbucks Corporation (SBUX)",
"T-Mobile US, Inc. (TMUS)",
"Target Corporation (TGT)",
"Tencent Holdings Limited (TCEHY)",
"Tesla, Inc. (TSLA)",
"The Boeing Company (BA)",
"The Coca-Cola Company (KO)",
"The Home Depot, Inc. (HD)",
"The Procter & Gamble Company (PG)",
"The Walt Disney Company (DIS)",
"Uber Technologies, Inc. (UBER)",
"Union Pacific Corporation (UNP)",
"United Parcel Service, Inc. (UPS)",
"United Technologies Corporation (UTX)",
"UnitedHealth Group Incorporated (UNH)",
"Verizon Communications Inc. (VZ)",
"Visa Inc. (V)",
"Walgreens Boots Alliance, Inc. (WBA)",
"Walmart Inc. (WMT)",
"Walt Disney Co. (DIS)",
"Walt Disney Company (DIS)",
"Wells Fargo & Company (WFC)",
"Zoom Video Communications, Inc. (ZM)"
];