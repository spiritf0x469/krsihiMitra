import { useState, useEffect } from "react";
import "./App.css";

function App() {

  const [state, setState] = useState("");
  const [season, setSeason] = useState("");

  const [options, setOptions] = useState({});
  const [states, setStates] = useState([]);
  const [seasons, setSeasons] = useState([]);

  const [area, setArea] = useState("");
  const [areaUnit, setAreaUnit] = useState("hectare");

  const [rainfall, setRainfall] = useState("");
  const [rainfallUnit, setRainfallUnit] = useState("mm");

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");


  // Convert area to hectares
  const convertArea = (value, unit) => {

    if (unit === "acre") {
      return value * 0.404686;
    }

    return value;
  };


  // Convert rainfall to millimetres
  const convertRainfall = (value, unit) => {

    if (unit === "cm") {
      return value * 10;
    }

    return value;
  };


  // Load states and their valid seasons
  useEffect(() => {

    const getOptions = async () => {

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/options"
        );

        const data = await response.json();

        setOptions(data);

        const availableStates = Object.keys(data);

        setStates(availableStates);

        if (availableStates.length > 0) {

          const firstState = availableStates[0];

          setState(firstState);

          setSeasons(data[firstState]);

          setSeason(data[firstState][0]);

        }

      } catch (error) {

        console.error(error);

        setMessage(
          "Could not load states and seasons."
        );

      }

    };

    getOptions();

  }, []);


  // Get crop recommendations
  const handleSubmit = async (e) => {

    e.preventDefault();

    setMessage("");
    setRecommendations([]);


    if (!state || !season) {

      setMessage(
        "Please select a state and season."
      );

      return;
    }


    if (!area || !rainfall) {

      setMessage(
        "Please enter area and rainfall."
      );

      return;
    }


    const areaInHectares = convertArea(
      Number(area),
      areaUnit
    );


    const rainfallInMM = convertRainfall(
      Number(rainfall),
      rainfallUnit
    );


    setLoading(true);


    try {

      const response = await fetch(
        "http://127.0.0.1:5000/recommend",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            state: state,
            season: season,
            area: areaInHectares,
            rainfall: rainfallInMM
          })
        }
      );


      const data = await response.json();


      if (!response.ok) {

        setMessage(
          data.error || "Something went wrong."
        );

        return;
      }


      if (
        !data.recommendations ||
        data.recommendations.length === 0
      ) {

        setMessage(
          "No crops found for this state and season."
        );

        return;
      }


      setRecommendations(
        data.recommendations
      );

    } catch (error) {

      console.error(error);

      setMessage(
        "Could not connect to backend."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="container">

      <h1>KrishiMitra🌾</h1>

      <p>
        Crop Recommendation System
      </p>


      <form onSubmit={handleSubmit}>


        {/* State */}

        <label>State</label>

        <select
          value={state}
          onChange={(e) => {

            const newState = e.target.value;

            setState(newState);

            setSeasons(
              options[newState]
            );

            setSeason(
              options[newState][0]
            );

          }}
        >

          {states.map((item) => (

            <option
              key={item}
              value={item}
            >

              {item.replace(
                /\b\w/g,
                (char) => char.toUpperCase()
              )}

            </option>

          ))}

        </select>


        {/* Season */}

        <label>Season</label>

        <select
          value={season}
          onChange={(e) =>
            setSeason(e.target.value)
          }
        >

          {seasons.map((item) => (

            <option
              key={item}
              value={item}
            >

              {item.replace(
                /\b\w/g,
                (char) => char.toUpperCase()
              )}

            </option>

          ))}

        </select>


        {/* Area */}

        <label>Area</label>

        <div className="input-row">

          <input
            type="number"
            min="0"
            value={area}
            onChange={(e) =>
              setArea(e.target.value)
            }
            placeholder="Enter area"
          />


          <select
            value={areaUnit}
            onChange={(e) =>
              setAreaUnit(e.target.value)
            }
          >

            <option value="hectare">
              Hectares
            </option>

            <option value="acre">
              Acres
            </option>

          </select>

        </div>


        {/* Rainfall */}

        <label>Annual Rainfall</label>

        <div className="input-row">

          <input
            type="number"
            min="0"
            value={rainfall}
            onChange={(e) =>
              setRainfall(e.target.value)
            }
            placeholder="Enter rainfall"
          />


          <select
            value={rainfallUnit}
            onChange={(e) =>
              setRainfallUnit(e.target.value)
            }
          >

            <option value="mm">
              mm
            </option>

            <option value="cm">
              cm
            </option>

          </select>

        </div>


        {/* Submit */}

        <button type="submit">

          {loading
            ? "Getting Recommendations..."
            : "Recommend Crops"}

        </button>

      </form>


      {/* Message */}

      {message && (

        <p className="message">
          {message}
        </p>

      )}


      {/* Calculations */}

      <div className="conversion-card">

        <h2>
          Calculations & Prediction
        </h2>


        <div className="formula">

          <strong>
            Area Conversion
          </strong>

          <p>
            1 acre = 0.404686 hectares
          </p>

          <p className="equation">
            Hectares = Acres × 0.404686
          </p>

        </div>


        <div className="formula">

          <strong>
            Rainfall Conversion
          </strong>

          <p>
            1 cm = 10 mm
          </p>

          <p className="equation">
            Rainfall (mm) = cm × 10
          </p>

        </div>


        <div className="formula">

          <strong>
            Predicted Yield
          </strong>

          <p>
            Random Forest Regression
          </p>

          <p className="equation">
            Predicted Yield = Average of 200 Tree Predictions
          </p>

        </div>

      </div>


      {/* Recommendations */}

      {recommendations.length > 0 && (

        <div className="results">

          <h2>
            Recommended Crops
          </h2>


          {recommendations.map((crop) => (

            <div
              className="crop-card"
              key={crop.rank}
            >

              <h3>
                #{crop.rank} {crop.Crop}
              </h3>

              <p>
                Predicted Yield:{" "}
                {crop.predicted_yield}
              </p>

            </div>

          ))}

        </div>

      )}


      {/* Footer */}

      <footer>
        © 2026 KrishiMitra. All rights reserved.
      </footer>


    </div>

  );

}

export default App;