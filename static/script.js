function drawGauge(ctx, value, max, label) {
  let start = -0.5 * Math.PI;
  let end = ((value / max) * 2 * Math.PI) - 0.5 * Math.PI;

  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  // Background circle
  ctx.beginPath();
  ctx.arc(ctx.canvas.width/2, ctx.canvas.height/2, ctx.canvas.width/2 - 15, 0, 2 * Math.PI);
  ctx.strokeStyle = "rgba(255,255,255,0.2)";
  ctx.lineWidth = 15;
  ctx.stroke();

  // Value arc
  ctx.beginPath();
  let gradient = ctx.createLinearGradient(0,0,200,0);
  gradient.addColorStop(0, "#00ff87");
  gradient.addColorStop(1, "#60efff");
  ctx.arc(ctx.canvas.width/2, ctx.canvas.height/2, ctx.canvas.width/2 - 15, start, end);
  ctx.strokeStyle = gradient;
  ctx.lineWidth = 15;
  ctx.lineCap = "round";
  ctx.stroke();

  // Text
  ctx.fillStyle = "#fff";
  ctx.font = "18px Poppins";
  ctx.textAlign = "center";
  ctx.fillText(label, ctx.canvas.width/2, ctx.canvas.height/2 - 10);
  ctx.font = "22px Poppins bold";
  ctx.fillText(value.toFixed(1), ctx.canvas.width/2, ctx.canvas.height/2 + 25);
}

// Animate gauge smoothly
function animateGauge(ctx, target, max, label) {
  let current = 0;
  let step = target / 50;
  let interval = setInterval(() => {
    if (current >= target) {
      current = target;
      clearInterval(interval);
    }
    drawGauge(ctx, current, max, label);
    current += step;
  }, 30);
}

document.getElementById("startBtn").addEventListener("click", async () => {
  document.getElementById("progressBar").style.display = "block";
  document.getElementById("startBtn").style.display = "none";
  document.getElementById("againBtn").style.display = "none";

  let progress = document.getElementById("progress");
  progress.style.width = "0%";

  let interval = setInterval(() => {
    let w = parseInt(progress.style.width);
    if (w < 90) progress.style.width = (w+2) + "%";
  }, 200);

  let res = await fetch("/run_test");
  let data = await res.json();

  clearInterval(interval);
  progress.style.width = "100%";
  setTimeout(() => { document.getElementById("progressBar").style.display = "none"; }, 500);

  // Animate gauges
  let dctx = document.getElementById("downloadGauge").getContext("2d");
  let uctx = document.getElementById("uploadGauge").getContext("2d");
  let pctx = document.getElementById("pingGauge").getContext("2d");

  animateGauge(dctx, data.download, 100, "Download");
  animateGauge(uctx, data.upload, 100, "Upload");
  animateGauge(pctx, data.ping, 300, "Ping");

  // Show test again button
  document.getElementById("againBtn").style.display = "inline-block";

  // Add result row
  let row = `<tr>
      <td>${data.date}</td>
      <td>${data.download.toFixed(2)} Mbps</td>
      <td>${data.upload.toFixed(2)} Mbps</td>
      <td>${data.ping.toFixed(2)} ms</td>
      <td>${data.server}</td>
    </tr>`;
  document.getElementById("resultsBody").insertAdjacentHTML("afterbegin", row);
});

// Restart test
document.getElementById("againBtn").addEventListener("click", () => {
  document.getElementById("startBtn").click();
});
