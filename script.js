document.addEventListener("DOMContentLoaded", () => {
  async function fetchData() {
    try {
      const res = await fetch("/data");
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      document.getElementById("pitcher").textContent = data.pitcher;
      document.getElementById("pitch-count").textContent = `P:${data.pitchCount}`;
      document.getElementById("batter").textContent = data.batter;
      document.getElementById("batting-stats").textContent = data.battingStats || "";
      document.getElementById("away-team").textContent = data.awayAbbr;
      document.getElementById("away-score").textContent = data.awayScore;
      document.getElementById("home-team").textContent = data.homeAbbr;
      document.getElementById("home-score").textContent = data.homeScore;
      document.querySelector(".inning-number").textContent = data.inningNumber;
      document.getElementById("inning").textContent = `${data.half} ${data.inningNumber}`;
      document.getElementById("count").textContent = `${data.balls}-${data.strikes}`;
      document.getElementById("outs").textContent = `${data.outs} OUT`;


      // Dynamic team logos (class-based)
      document.getElementById("away-logo").className = `bbclub-${data.awayAbbr}`;
      document.getElementById("home-logo").className = `bbclub-${data.homeAbbr}`;

      // Dynamic background/text color
      document.getElementById("away").className = `team away team-bg-${data.awayAbbr}`;
      document.getElementById("home").className = `team home team-bg-${data.homeAbbr}`;

      // Update bases individually
      document.getElementById("base-first").classList.toggle("occupied", data.bases[0]);
      document.getElementById("base-second").classList.toggle("occupied", data.bases[1]);
      document.getElementById("base-third").classList.toggle("occupied", data.bases[2]);
    } catch (err) {
      console.error("Error loading scoreboard:", err);
    }
  }

  fetchData();
  setInterval(fetchData, 10000); // Refresh every 10s
});
