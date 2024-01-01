// Define tickers in the outer scope
let tickers = [];
let is_logged_in = false;

var lastPrices = {};
var counter = 15;

async function watchlistCreation() {

    await fetch(`/get_user_watchlist`)
        .then(response => response.json())
        .then(data => {
            if (data.login === 'true') {
                is_logged_in = true;
                tickers = data.watchlist || [];
            }
        })
        .catch(error => console.error('Error:', error));


    tickers.forEach((ticker) => {
        addTickerToGrid(ticker);
        console.log(ticker);
    })

    updatePrices();

    startUpdateCycle();

}
watchlistCreation()

const startUpdateCycle = () => {
    updatePrices();
    setInterval(() => {
        counter--;
        if (counter <= 0) {
            updatePrices();
            counter = 15;
        }
    }, 1000)
}

$(document).ready(() => {

    $("#add-ticker-form").submit((e) => {
        e.preventDefault();

        if (is_logged_in) {
            var newTicker = $('#new-ticker').val().toUpperCase();
            if (!tickers.includes(newTicker)) {
                tickers.push(newTicker);

                fetch('/add_to_watchlist', {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'POST',
                    body: JSON.stringify({
                        Stock: newTicker
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                    });

                addTickerToGrid(newTicker);
            }
            $('new-ticker').val('');
            updatePrices();
        }
        else {
            $('new-ticker').val('');

            window.location.href = "/register";
        }
    })

    $('#tickers-grid').on('click', '.remove-btn', function () {
        e.preventDefault();

        if (is_logged_in) {
            var tickerToRemove = $(this).data('ticker');

            fetch('/remove_from_watchlist', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    Stock: tickerToRemove
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                });

            $(`#${tickerToRemove}`).remove();
        }
        else {
            window.location.href = "/register";
        }
    });

});

const addTickerToGrid = (ticker) => {
    $('#tickers-grid').append(`<div id="${ticker}" class="stock-box"><h2>${ticker}</h2>
        <p id="${ticker}-price"></p><p id="${ticker}-pct"></p>
        <button class="remove-btn" data-ticker="${ticker}">Remove</button></div>`)

}
const updatePrices = () => {
    tickers.forEach((ticker) => {
        $.ajax({
            url: '/display_watchlist',
            type: "POST",
            data: JSON.stringify({
                'ticker': ticker
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: (data) => {
                var changePercent = ((data.currentPrice - data.openPrice) / data.openPrice) * 100;
                var colorclass;
                if (changePercent <= -2) {
                    colorclass = 'dark-red';
                }
                else if (changePercent < 0) {
                    colorclass = 'red';
                }
                else if (changePercent == 0) {
                    colorclass = 'gray';
                }
                else if (changePercent <= 2) {
                    colorclass = 'green';
                }
                else {
                    colorclass = 'dark-green';
                }

                $(`#${ticker}-price`).text(`$${data.currentPrice.toFixed(2)}`);
                $(`#${ticker}-pct`).text(`${changePercent.toFixed(2)}%`);

                $(`#${ticker}-price`).removeClass(`dark-red red gray green dark-green`).addClass(colorclass);
                $(`#${ticker}-pct`).removeClass(`dark-red red gray green dark-green`).addClass(colorclass);

                var flaskClass;
                if (lastPrices[ticker] > data.currentPrice) {
                    flaskClass = 'red-flask';
                } else if (lastPrices[ticker] < data.currentPrice) {
                    flaskClass = 'green-flask';
                }
                else {
                    flaskClass = 'gray-flask'
                }
                lastPrices[ticker] = data.currentPrice;

                $(`#${ticker}`).addClass(flaskClass);
                setTimeout(() => {
                    $(`#${ticker}`).removeClass(flaskClass);
                }, 1000);
            }
        });
    });
}