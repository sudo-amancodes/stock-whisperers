const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");
let webLink;

// if user press any key and release
inputBox.onkeyup = (e) => {
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if (userData) {
        icon.onclick = () => {
            webLink = `https://www.google.com/search?q=${userData}`;
            linkTag.setAttribute("href", webLink);
            linkTag.click();
        }
        emptyArray = suggestions.filter((data) => {
            //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data) => {
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
    } else {
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
}

function select(element) {
    let selectData = element.textContent;
    inputBox.value = selectData;
    var regExp = /\(([^)]+)\)/;
    var stock_ticker = regExp.exec(inputBox.value);
    fetch('/data', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            Stock: stock_ticker[1]
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

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    } else {
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