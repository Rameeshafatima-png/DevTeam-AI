const $ = (id) => document.getElementById(id);
const requirement = $("requirement");
const buildBtn = $("buildBtn");
const results = $("results");
const loading = $("loading");
const errorBox = $("errorBox");
let currentData = null;
let activeTab = "plan";

const tabMap = {
  plan: ["IMPLEMENTATION_PLAN.MD", "plan"],
  code: ["SOLUTION.PY", "code"],
  tests: ["TEST_SOLUTION.PY", "tests"],
  review: ["CODE_REVIEW.MD", "review"],
  report: ["DEVELOPMENT_REPORT.MD", "report"]
};

requirement.addEventListener("input", () => {
  $("charCount").textContent = `${requirement.value.length} / 6000`;
});
document.querySelectorAll(".example-chip").forEach(btn => {
  btn.addEventListener("click", () => {
    requirement.value = btn.dataset.example;
    requirement.dispatchEvent(new Event("input"));
    requirement.focus();
  });
});

$("themeToggle").addEventListener("click", () => document.body.classList.toggle("light"));

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    $("apiStatus").textContent = data.groq_configured ? `Connected · ${data.model}` : "Add Groq API key";
  } catch {
    $("apiStatus").textContent = "API unavailable";
  }
}
checkHealth();

buildBtn.addEventListener("click", async () => {
  const text = requirement.value.trim();
  errorBox.classList.add("hidden");
  results.classList.add("hidden");
  if (text.length < 20) {
    showError("Please enter a software requirement with at least 20 characters.");
    requirement.focus();
    return;
  }
  buildBtn.disabled = true;
  loading.classList.remove("hidden");
  loading.scrollIntoView({behavior:"smooth", block:"center"});
  try {
    const response = await fetch("/api/build", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({requirement:text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The build could not be completed.");
    currentData = data;
    $("downloadBtn").href = data.download_url;
    $("resultSubtitle").textContent = `Project ${data.project_id} · ${data.files.length} generated deliverables`;
    const tr = data.test_results || {};
    $("testStatus").textContent = `TEST EXECUTION: ${(tr.status || "unknown").toUpperCase()}  ·  Passed: ${tr.passed ?? 0}  ·  Failed: ${tr.failed ?? 0}`;
    results.classList.remove("hidden");
    selectTab("plan");
    results.scrollIntoView({behavior:"smooth", block:"start"});
  } catch (err) {
    showError(err.message);
  } finally {
    loading.classList.add("hidden");
    buildBtn.disabled = false;
  }
});

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
  errorBox.scrollIntoView({behavior:"smooth", block:"center"});
}
function selectTab(tab) {
  activeTab = tab;
  document.querySelectorAll(".tab").forEach(btn => btn.classList.toggle("active", btn.dataset.tab === tab));
  const [title, key] = tabMap[tab];
  $("outputTitle").textContent = title;
  $("outputContent").textContent = currentData?.[key] || "No content returned for this section.";
}
document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => selectTab(btn.dataset.tab)));
$("copyBtn").addEventListener("click", async () => {
  if (!currentData) return;
  await navigator.clipboard.writeText(currentData[tabMap[activeTab][1]] || "");
  $("copyBtn").textContent = "Copied!";
  setTimeout(() => $("copyBtn").textContent = "Copy content", 1300);
});
