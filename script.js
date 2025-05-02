async function submitResume() {
    const resumeFile = document.getElementById("resumeInput").files[0];
    const jobDesc = document.getElementById("jobDescription").value;
  
    if (!resumeFile) {
      alert("Please upload a resume.");
      return;
    }
  
    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDesc);
  
    const response = await fetch("http://127.0.0.1:5000/scan", {
      method: "POST",
      body: formData,
    });
  
    const result = await response.json();
  
    // Update UI with name, match score, and skills
    document.getElementById("name").innerText = result.name.toUpperCase();
    document.getElementById("matchScore").innerText = result.match_score.toFixed(2) + "%";
  
    const skillsList = document.getElementById("skills");
    skillsList.innerHTML = "";
    result.skills_found.forEach(skill => {
      const li = document.createElement("li");
      li.innerText = skill;
      skillsList.appendChild(li);
    });
  }
  