/* app jsx */
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api";

function App() {
  const [people, setPeople] = useState([]);
  const [selectedPerson, setSelectedPerson] = useState("");
  const [skills, setSkills] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [companies, setCompanies] = useState([]);

  const [loadingPeople, setLoadingPeople] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState("");

  // Load all people
  useEffect(() => {
    fetch(`${API_URL}/people/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load people");
        }

        return response.json();
      })
      .then((data) => {
        setPeople(data.people);
      })
      .catch(() => {
        setError("Unable to connect to SkillConnect.");
      })
      .finally(() => {
        setLoadingPeople(false);
      });
  }, []);

  // Load selected person's graph data
  const loadPersonDetails = async (name) => {
    setSelectedPerson(name);
    setLoadingDetails(true);
    setError("");

    try {
      const [skillsResponse, jobsResponse, companiesResponse] =
        await Promise.all([
          fetch(`${API_URL}/people/${name}/skills/`),
          fetch(`${API_URL}/people/${name}/recommendations/`),
          fetch(`${API_URL}/people/${name}/companies/`),
        ]);

      if (
        !skillsResponse.ok ||
        !jobsResponse.ok ||
        !companiesResponse.ok
      ) {
        throw new Error("Failed to load profile");
      }

      const skillsData = await skillsResponse.json();
      const jobsData = await jobsResponse.json();
      const companiesData = await companiesResponse.json();

      setSkills(skillsData.skills);
      setRecommendations(jobsData.recommendations);
      setCompanies(companiesData.matches);
    } catch (error) {
      console.error(error);
      setError("Unable to load this person's recommendations.");
    } finally {
      setLoadingDetails(false);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div>
          <h1>SkillConnect</h1>
          <p>
            Discover career opportunities through skill connections.
          </p>
        </div>
      </header>

      <main className="container">

        {/* Hero section */}
        <section className="hero">
          <span className="badge">
            GRAPH-POWERED CAREER EXPLORER
          </span>

          <h2>
            Find jobs and companies
            <br />
            connected to your skills.
          </h2>

          <p>
            Select a person to explore their skills, matching jobs,
            and companies through the SkillConnect graph.
          </p>
        </section>

        {/* Error */}
        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {/* People */}
        <section className="people-section">

          <div className="section-title">
            <div>
              <h3>Choose a profile</h3>

              <p>
                Select a person to explore their career graph.
              </p>
            </div>
          </div>

          {loadingPeople ? (
            <div className="loading">
              Loading profiles...
            </div>
          ) : people.length === 0 ? (
            <div className="empty">
              No people found.
            </div>
          ) : (
            <div className="people-grid">

              {people.map((person) => (
                <button
                  className={`person-card ${
                    selectedPerson === person.name ? "active" : ""
                  }`}
                  key={person.name}
                  onClick={() => loadPersonDetails(person.name)}
                >

                  <div className="avatar">
                    {person.name.charAt(0)}
                  </div>

                  <div>
                    <strong>{person.name}</strong>

                    <span>
                      View career graph →
                    </span>
                  </div>

                </button>
              ))}

            </div>
          )}

        </section>

        {/* Results */}
        {selectedPerson && (
          <section className="results">

            {/* Profile heading */}
            <div className="profile-heading">

              <div className="large-avatar">
                {selectedPerson.charAt(0)}
              </div>

              <div>
                <span>CAREER GRAPH</span>

                <h2>
                  {selectedPerson}
                </h2>
              </div>

            </div>

            {loadingDetails ? (
              <div className="loading">
                Exploring graph connections...
              </div>
            ) : (
              <>

                {/* Result cards */}
                <div className="cards">

                  {/* Skills */}
                  <div className="result-card">

                    <span className="card-label">
                      YOUR SKILLS
                    </span>

                    <h3>
                      {skills.length}
                    </h3>

                    <div className="tags">

                      {skills.map((skill) => (
                        <span
                          className="tag"
                          key={skill.skill}
                        >
                          {skill.skill}
                        </span>
                      ))}

                    </div>

                  </div>

                  {/* Jobs */}
                  <div className="result-card">

                    <span className="card-label">
                      MATCHING JOBS
                    </span>

                    <h3>
                      {recommendations.length}
                    </h3>

                    <ul>

                      {recommendations.map((job) => (
                        <li key={job.job}>
                          {job.job}
                        </li>
                      ))}

                    </ul>

                  </div>

                  {/* Companies */}
                  <div className="result-card">

                    <span className="card-label">
                      MATCHING COMPANIES
                    </span>

                    <h3>
                      {companies.length}
                    </h3>

                    <ul>

                      {companies.map((item, index) => (
                        <li
                          key={`${item.company}-${item.job}-${index}`}
                        >

                          <strong>
                            {item.company}
                          </strong>

                          <small>
                            {item.job}
                          </small>

                        </li>
                      ))}

                    </ul>

                  </div>

                </div>

                {/* Graph explanation */}
                <div className="graph-explanation">

                  <span>
                    HOW THE GRAPH CONNECTS
                  </span>

                  <div className="path">

                    <div>PERSON</div>

                    <span>→</span>

                    <div>SKILL</div>

                    <span>→</span>

                    <div>JOB</div>

                    <span>→</span>

                    <div>COMPANY</div>

                  </div>

                  <p>
                    SkillConnect follows relationships between people,
                    skills, jobs, and companies instead of treating
                    them as isolated records.
                  </p>

                </div>

              </>
            )}

          </section>
        )}

      </main>

    </div>
  );
}

export default App;
