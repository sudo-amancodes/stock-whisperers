var chart = LightweightCharts.createChart(document.getElementById('chart-container'), {
    width: document.getElementById('chart-container').clientWidth,
    height: 550
});

var candleSeries = chart.addCandlestickSeries();

chart.applyOptions({
    timeScale: {
        timeVisible: true,
        secondsVisible: true
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    }
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
socket.on('updateSensorData', (new_value) => {
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

$('#sendBtn').on('click', function () {
    socket.send($('#comment-input').val());
    $('#comment-input').val('');
});

socket.on("message", (data) => {
    $("#comments-container").append($("<div>").html(`<strong>${data.username}:</strong>${data.content}`));
});

socket.on('redirect', function (data) {
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
