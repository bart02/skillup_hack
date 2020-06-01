var curr_telemetry;
var freq = 4;
var choosing = false;
var cursor;
var choose_type;
var choose_id;
var adding_point = false;
var adding_line = false;
var remove_point = false;
var remove_line = false;
var roads;
let low_voltage = 3.8;

function get_telemetry() {
    let request = new XMLHttpRequest();
    request.open('GET', '/get', false);
    request.send();
    if (request.status === 200) {
        return JSON.parse(request.responseText)["drones"];
    } else {
        return null;
    }
}

function update() {
    let data = get_telemetry();
    let list = document.getElementById("drones-list");
    if (data !== null) {
        curr_telemetry = data;
        drawDrones();
        while (list.childElementCount / 2 > data.length) {
            removeLabel((list.childElementCount / 2 - 1).toString());
        }

        while (list.childElementCount / 2 < data.length) {
            addLabel((list.childElementCount / 2).toString());
        }

        for (let i = 0; i < data.length; i++) {
            render_drone(data[i], (i).toString());
        }
    }
}

function render_drone(el, id) {
    if (el.status === "land") {
        document.getElementById(id + "img").src = "/static/svg/drone.svg";
    } else {
        document.getElementById(id + "img").src = "/static/svg/flying_drone.svg";
    }
    document.getElementById(id + "colorpicker").style.backgroundColor = el.led;
    document.getElementById(id + "ip").innerHTML = el.ip;
    document.getElementById(id + "x").innerHTML = "x: " + (Math.round(el.pose.x * 100) / 100).toString();
    document.getElementById(id + "y").innerHTML = "y: " + (Math.round(el.pose.y * 100) / 100).toString();
    document.getElementById(id + "z").innerHTML = "z: " + (Math.round(el.pose.z * 100) / 100).toString();
    if ((Math.round(el.voltage * 100) / 100) <= low_voltage) {
        document.getElementById(id + "voltage").style.color = "#f22234";
    } else {
        document.getElementById(id + "voltage").style.color = "#55942f"
    }
    document.getElementById(id + "voltage").innerHTML = "<strong>" + (Math.round(el.voltage * 100) / 100).toString() + " V</strong>";
    document.getElementById(id + "nx").innerHTML = "x: " + (Math.round(el.nextp.pose.x * 100) / 100).toString();
    document.getElementById(id + "ny").innerHTML = "y: " + (Math.round(el.nextp.pose.y * 100) / 100).toString();
    document.getElementById(id + "nz").innerHTML = "z: " + (Math.round(el.nextp.pose.z * 100) / 100).toString();
}

function updateCycle() {
    setTimeout(function () {
        try {
            update();
        } catch (e) {

        }
        updateCycle();
    }, 1000 / freq);
}

function addLabel(id, el) {
    document.getElementById("drones-list").innerHTML += "<div id='" + id + "' class='drone-el'><div><img id='" + id
        + "img' class='drone-img' alt='' src=''/><div class='elbut delet' onclick='delet(" + id + ")'>" +
        "Delete</div></div><div class='elcontento'><div class='full'><strong>Current Pose</strong>" +
        "<div><div id='" + id + "x'></div><div id='" + id + "y'></div><div id='" + id + "z'></div><div class='ip' id='" + id + "ip'></div></div></div>" +
        "<div class='full'><strong>Next Pose</strong>" +
        "<div><div id='" + id + "nx'></div><div id='" + id + "ny'></div><div id='" + id + "nz'></div>" +
        "<div class ='voltage' id = '" + id + "voltage'></div></div>" +
        "</div><div class='elbutto'>" +
        "<div onclick='land(" + id + ")' class='elbut' style='margin: 8px 8px 4px 8px;'>" +
        "Arrived</div><div class='elbut' onclick='flyto(" + id + ")' style='margin: 4px 8px 8px 8px;'>" +
        "Go to</div></div>" +
        "</div>" +
        "<div class='colorel' id='" + id + "colorpicker'></div></div><hr id='" + id + "hr' />";
    /*id='" + id + "color'*/
    $(".colorel").spectrum({
        color: "#000",
        preferredFormat: 'rgb'
    });
    $(".colorel").on('hide.spectrum', function (e, tinycolor) {
        let request = new XMLHttpRequest();
        request.open('GET', '/set_color?id=' + parseInt(e.currentTarget.id) + '&color=' + toHex(tinycolor._r) + toHex(tinycolor._g) + toHex(tinycolor._b), false);
        request.send();
    });
}

function toHex(c) {
    let col = Math.round(c).toString(16);
    while (col.length < 2)
        col = '0' + col;
    return col
}

function land(i) {
    let request = new XMLHttpRequest();
    let send_data = {
        id: i,
        command: 'arrived'
    };
    request.open('GET', '/send?' + Object.entries(send_data).map(e => e.join('=')).join('&'), true);
    request.send(null);
}

function force_land() {
    for (let i = 0; i < curr_telemetry.length; i++) {
        let request = new XMLHttpRequest();
        let send_data = {
            id: i,
            command: 'force_land',
            x: curr_telemetry[i].pose.x,
            y: curr_telemetry[i].pose.y,
            z: 2
        };
        request.open('GET', '/send?' + Object.entries(send_data).map(e => e.join('=')).join('&'), true);
        request.send(null);
    }
}

function flyto(id) {
    choose_id = parseInt(id);
    choosing = true;
    adding_point = false;
    adding_line = false;
    remove_point = false;
    remove_line = false;
    choose_type = "fly";
    canvas.backgroundColor = "#bdbdbd";
    for (let i = 0; i < canvas._objects.length; i++) {
        canvas._objects[i].set('opacity', 0.8);
    }
    canvas.renderAll();
}

function delet(id) {
    Ply.dialog(
        "confirm",
        "Delete Clever from this list?"
    ).done(function (ui) {
        let request = new XMLHttpRequest();
        request.open('GET', '/delete?id=' + id, false);
        request.send();
    })
        .fail(function (ui) {
        });

}

function removeLabel(id) {
    let element = document.getElementById(id);
    element.parentNode.removeChild(element);
    let element2 = document.getElementById(id + "hr");
    element2.parentNode.removeChild(element2);
}

function refreshh() {
    for (let i = 0; i < curr_telemetry.length; i++) {
        let request = new XMLHttpRequest();
        request.open('GET', '/delete?id=0', false);
        request.send();
    }

}