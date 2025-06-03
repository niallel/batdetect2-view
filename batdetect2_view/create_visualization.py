import json
from datetime import datetime
import os

def load_data(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def create_html_visualization(data, output_file='bat_detections.html'):
    # Extract data for visualizations
    timestamps = []
    species = {}
    det_probs = []
    class_probs = []  # Add class probabilities
    hours = [0] * 24  # Count of detections per hour
    species_list = []  # Store species for each detection
    high_freqs = []  # Store high frequencies
    low_freqs = []   # Store low frequencies
    
    # Mapping of scientific names to common names
    species_names = {
        'Myotis mystacinus': 'Whiskered Bat',
        'Myotis brandtii': "Brandt's Bat",
        'Myotis daubentonii': "Daubenton's Bat",
        'Myotis nattereri': "Natterer's Bat",
        'Myotis bechsteinii': "Bechstein's Bat",
        'Myotis alcathoe': "Alcathoe Bat",
        'Myotis myotis': 'Greater Mouse-eared Bat',
        'Myotis blythii': 'Lesser Mouse-eared Bat',
        'Pipistrellus pipistrellus': 'Common Pipistrelle',
        'Pipistrellus pygmaeus': 'Soprano Pipistrelle',
        'Pipistrellus nathusii': "Nathusius' Pipistrelle",
        'Pipistrellus kuhlii': "Kuhl's Pipistrelle",
        'Nyctalus noctula': 'Noctule',
        'Nyctalus leisleri': "Leisler's Bat",
        'Nyctalus lasiopterus': 'Greater Noctule',
        'Eptesicus serotinus': 'Serotine',
        'Eptesicus nilssonii': 'Northern Bat',
        'Vespertilio murinus': 'Parti-coloured Bat',
        'Barbastella barbastellus': 'Barbastelle',
        'Barbastellus barbastellus': 'Barbastelle',
        'Plecotus auritus': 'Brown Long-eared Bat',
        'Plecotus austriacus': 'Grey Long-eared Bat',
        'Rhinolophus hipposideros': 'Lesser Horseshoe Bat',
        'Rhinolophus ferrumequinum': 'Greater Horseshoe Bat',
        'Rhinolophus euryale': 'Mediterranean Horseshoe Bat',
        'Rhinolophus mehelyi': "Mehely's Horseshoe Bat",
        'Rhinolophus blasii': "Blasius' Horseshoe Bat",
        'Miniopterus schreibersii': "Schreiber's Bat",
        'Tadarida teniotis': 'European Free-tailed Bat'
    }
    
    for detection in data['annotation']:
        # Convert timestamp to datetime
        dt = datetime.fromtimestamp(detection['start_time'])
        timestamps.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
        
        # Store species and count
        species_name = detection['class']
        species[species_name] = species.get(species_name, 0) + 1
        species_list.append(species_name)
        
        # Collect both probabilities
        det_probs.append(detection['det_prob'])
        class_probs.append(detection['class_prob'])
        
        # Count by hour
        hours[dt.hour] += 1
        
        # Collect high and low frequencies
        high_freqs.append(detection['high_freq'])
        low_freqs.append(detection['low_freq'])

    # Calculate date range
    if timestamps:
        start_date = datetime.strptime(timestamps[0], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(timestamps[-1], '%Y-%m-%d %H:%M:%S')
        # Get local timezone
        local_tz = datetime.now().astimezone().tzinfo
        date_range = f"{start_date.strftime('%Y-%m-%d %H:%M')} to {end_date.strftime('%Y-%m-%d %H:%M')} ({local_tz})"
    else:
        date_range = "No data available"

    # Create HTML with Chart.js and D3
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Bat Detection Analysis</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1280 585'><g transform='translate(0,585) scale(0.1,-0.1)' fill='%23000' stroke='none'><path d='M9785 5728 c-2 -7 -22 -68 -45 -135 -313 -948 -940 -1649 -1822-2037 -209 -92 -598 -211 -618 -189 -4 4 -47 209 -96 456 -49 246 -92 446 -96 445 -4 -2 -93 -85 -197 -186 l-190 -182 -48 30 c-86 55 -167 73 -301 67 -75 -3 -135 -11 -166 -22 l-49 -18 -177 184 -177 184 -26 -85 c-14 -47 -83 -276 -152 -510 -69 -234 -131 -440 -136 -458 -13 -40 -11 -40 -214 25 -834 270-1466 781-1894 1533 -119 210 -278 599 -306 753 -4 20 -11 37 -15 37 -4 0-25 -21-46 -47 -59 -73 -199 -219 -294 -307 -463 -431 -1050 -712 -1700 -815 -151 -24 -345 -41 -483 -42 l-102 0 110 -23 c694 -145 1141 -501 1270 -1010 13 -50 26 -126 30 -169 6 -63 10 -77 22 -73 37 15 183 48 290 67 149 26 427 36 544 20 414 -59 707 -271 890 -646 67 -137 110 -263 139 -403 22 -112 40 -248 40 -308 l0 -42 92 55 c106 64 190 101 314 140 83 25 102 27 264 27 161 0 182 -2 265 -27 119 -36 288 -120 400 -199 111 -78 344 -308 454 -446 97 -123 245 -344 336 -502 77 -133 237 -457 286 -579 l34 -84 13 49 c126 473 374 815 792 1093 392 262 930 443 1499 506 80 8 145 17 146 18 1 1 12 56 24 122 138 724 488 1210 991 1374 267 88 596 92 886 11 64 -17 64 -17 68 4 30 154 92 301 178 423 160 227 434 471 793 705 200 131 357 220 635 361 140 71 247 127 238 123 -10 -3 -71 -13 -135 -23 -183 -27 -599 -24 -793 6 -383 58 -703 159 -1057 331 -252 122 -474 255 -646 387 -39 30 -59 40 -62 31z'/></g></svg>"/>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@1.0.1/dist/chartjs-adapter-moment.min.js"></script>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
    <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .header h1 {{
            margin: 0;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .header h1 i {{
            color: #666;
            font-size: 1.2em;
            vertical-align: middle;
        }}
        .date-range {{
            color: #666;
            font-size: 1.1em;
            text-align: center;
            flex-grow: 1;
            margin: 0 20px;
        }}
        .date-range input {{
            padding: 8px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 300px;
        }}
        .filter-container {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .filter-group {{
            display: flex;
            align-items: center;
            gap: 5px;
            margin: 5px;
        }}
        .content {{
            margin-top: 100px;
            padding: 20px;
        }}
        .chart-container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            padding: 10px;
        }}
        .hour-charts-container {{
            display: flex;
            gap: 20px;
            margin: 10px 0;
        }}
        .hour-chart {{
            flex: 1;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 10px;
        }}
        @media (max-width: 800px) {{
            .hour-charts-container {{
                flex-direction: column;
            }}
        }}
        h2 {{
            color: #333;
            margin-top: 0;
        }}
        select {{
            padding: 8px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
        label {{
            font-weight: bold;
            margin-right: 10px;
        }}
        .species-legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-right: 15px;
        }}
        .legend-color {{
            width: 15px;
            height: 15px;
            margin-right: 5px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1><span style="display:inline-block;vertical-align:middle;line-height:1;margin-right:8px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="0.9em" viewBox="0 0 1280 585" style="vertical-align:middle;">
                <g transform="translate(0,585) scale(0.1,-0.1)" fill="#000" stroke="none">
                    <path d="M9785 5728 c-2 -7 -22 -68 -45 -135 -313 -948 -940 -1649 -1822-2037 -209 -92 -598 -211 -618 -189 -4 4 -47 209 -96 456 -49 246 -92 446 -96 445 -4 -2 -93 -85 -197 -186 l-190 -182 -48 30 c-86 55 -167 73 -301 67 -75 -3 -135 -11 -166 -22 l-49 -18 -177 184 -177 184 -26 -85 c-14 -47 -83 -276 -152 -510 -69 -234 -131 -440 -136 -458 -13 -40 -11 -40 -214 25 -834 270-1466 781-1894 1533 -119 210 -278 599 -306 753 -4 20 -11 37 -15 37 -4 0-25 -21-46 -47 -59 -73 -199 -219 -294 -307 -463 -431 -1050 -712 -1700 -815 -151 -24 -345 -41 -483 -42 l-102 0 110 -23 c694 -145 1141 -501 1270 -1010 13 -50 26 -126 30 -169 6 -63 10 -77 22 -73 37 15 183 48 290 67 149 26 427 36 544 20 414 -59 707 -271 890 -646 67 -137 110 -263 139 -403 22 -112 40 -248 40 -308 l0 -42 92 55 c106 64 190 101 314 140 83 25 102 27 264 27 161 0 182 -2 265 -27 119 -36 288 -120 400 -199 111 -78 344 -308 454 -446 97 -123 245 -344 336 -502 77 -133 237 -457 286 -579 l34 -84 13 49 c126 473 374 815 792 1093 392 262 930 443 1499 506 80 8 145 17 146 18 1 1 12 56 24 122 138 724 488 1210 991 1374 267 88 596 92 886 11 64 -17 64 -17 68 4 30 154 92 301 178 423 160 227 434 471 793 705 200 131 357 220 635 361 140 71 247 127 238 123 -10 -3 -71 -13 -135 -23 -183 -27 -599 -24 -793 6 -383 58 -703 159 -1057 331 -252 122 -474 255 -646 387 -39 30 -59 40 -62 31z"/>
                </g>
            </svg>
        </span>Bat Detection Analysis</h1>
        <div class="date-range">
            <input type="text" id="dateRange" placeholder="Select date range...">
        </div>
        <div class="filter-container">
            <div class="filter-group">
                <label for="probFilter">Probability Filter:</label>
                <select id="probFilter" onchange="updateCharts()">
                    <option value="0,0">All</option>
                    {''.join(f'<option value="{threshold},0">Detections > {int(threshold*100)}% ({sum(1 for p in det_probs if p >= threshold)})</option>'
                    for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                    if sum(1 for p in det_probs if p >= threshold) > 0)}
                    {''.join(f'<option value="0,{threshold}">Species > {int(threshold*100)}% ({sum(1 for p in class_probs if p >= threshold)})</option>'
                    for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                    if sum(1 for p in class_probs if p >= threshold) > 0)}
                </select>
            </div>
        </div>
    </div>
    
    <div class="content">
        <div class="hour-charts-container">
            <div class="hour-chart">
                <h2>Detections by Hour of Day</h2>
                <canvas id="hourChart"></canvas>
            </div>
            <div class="hour-chart">
                <h2>Species by Hour of Day</h2>
                <canvas id="speciesHourChart"></canvas>
            </div>
        </div>

        <div class="chart-container">
            <h2>Detections Over Time (Detection Probability)</h2>
            <div id="timeChart"></div>
        </div>

        <div class="chart-container">
            <h2>Detections Over Time (Species Probability)</h2>
            <div id="speciesTimeChart"></div>
            <div id="speciesTimeLegend" class="species-legend"></div>
        </div>

        <div class="chart-container">
            <h2>Detections Over Time (Frequency)</h2>
            <div id="freqTimeChart"></div>
            <div id="freqTimeLegend" class="species-legend"></div>
        </div>

        <div class="chart-container">
            <h2 style="margin: 0 0 10px 0;">Species Distribution</h2>
            <div style="max-width: 1000px; margin: 0 auto;">
                <canvas id="speciesChart" width="400" height="250"></canvas>
            </div>
        </div>

        <div class="chart-container">
            <h2>Probability Distributions</h2>
            <canvas id="probChart"></canvas>
        </div>

        <div class="chart-container">
            <h2>Frequency Distribution</h2>
            <canvas id="freqDistChart"></canvas>
        </div>
    </div>

    <script>
        // Store the original data
        const originalData = {{
            timestamps: {json.dumps(timestamps)},
            species: {json.dumps(species_list)},
            det_probs: {json.dumps(det_probs)},
            class_probs: {json.dumps(class_probs)},
            hours: {json.dumps(hours)},
            high_freqs: {json.dumps(high_freqs)},
            low_freqs: {json.dumps(low_freqs)}
        }};

        // Initialize date range picker
        const firstTime = new Date(originalData.timestamps[0]);
        const lastTime = new Date(originalData.timestamps[originalData.timestamps.length - 1]);
        
        flatpickr("#dateRange", {{
            mode: "range",
            dateFormat: "Y-m-d H:i",
            enableTime: true,
            time_24hr: true,
            defaultDate: [firstTime, lastTime],
            minDate: firstTime,
            maxDate: lastTime,
            onChange: function(selectedDates) {{
                if (selectedDates.length === 2) {{
                    updateCharts();
                }}
            }}
        }});

        // Mapping of scientific names to common names
        const speciesNames = {json.dumps(species_names)};

        // Create a consistent color mapping for species
        const speciesColors = {{}};
        Object.keys(speciesNames).forEach((species, index) => {{
            const hue = (index * 137.5) % 360; // Golden angle approximation
            speciesColors[species] = `hsla(${{hue}}, 70%, 65%, 0.7)`;
        }});

        // Initialize charts
        let speciesChart, probChart, hourChart, speciesHourChart, freqDistChart;

        function createSpeciesChart(data) {{
            // Destroy existing chart if it exists
            if (speciesChart) {{
                speciesChart.destroy();
            }}

            // Convert data to array of objects if it's not already
            const chartData = Array.isArray(data) ? data : Object.entries(data).map(([key, value]) => ({{
                label: key,
                value: value
            }}));

            // Add common names to labels
            chartData.forEach(d => {{
                if (speciesNames[d.label]) {{
                    d.label = `${{d.label}} (${{speciesNames[d.label]}})`;
                }}
            }});

            // Create pie chart
            speciesChart = new Chart(document.getElementById('speciesChart'), {{
                type: 'pie',
                data: {{
                    labels: chartData.map(d => d.label),
                    datasets: [{{
                        data: chartData.map(d => d.value),
                        backgroundColor: chartData.map(d => speciesColors[d.label.split(' (')[0]])
                    }}]
                }},
                options: {{
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{
                                generateLabels: function(chart) {{
                                    const data = chart.data;
                                    if (data.labels.length && data.datasets.length) {{
                                        return data.labels.map(function(label, i) {{
                                            const value = data.datasets[0].data[i];
                                            return {{
                                                text: `${{label}} (${{value}})`,
                                                fillStyle: data.datasets[0].backgroundColor[i],
                                                hidden: isNaN(data.datasets[0].data[i]),
                                                lineCap: 'butt',
                                                lineDash: [],
                                                lineDashOffset: 0,
                                                lineJoin: 'miter',
                                                lineWidth: 1,
                                                strokeStyle: '#fff',
                                                pointStyle: 'circle',
                                                rotation: 0
                                            }};
                                        }});
                                    }}
                                    return [];
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}

        // Create D3 time series chart
        function createTimeChart(data, isSpeciesProb = false, isFreq = false) {{
            const chartId = isFreq ? 'freqTimeChart' : (isSpeciesProb ? 'speciesTimeChart' : 'timeChart');
            const margin = {{top: 20, right: 30, bottom: 90, left: 80}};
            const width = document.getElementById(chartId).clientWidth - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;

            // Clear previous chart
            d3.select(`#${{chartId}}`).selectAll("*").remove();
            if (isSpeciesProb || isFreq) {{
                // Clear previous legend
                document.getElementById(isFreq ? 'freqTimeLegend' : 'speciesTimeLegend').innerHTML = '';
            }}

            // Create SVG
            const svg = d3.select(`#${{chartId}}`)
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

            // Create scales
            const firstTime = new Date(data.timestamps[0]);
            const lastTime = new Date(data.timestamps[data.timestamps.length - 1]);

            const x = d3.scaleTime()
                .domain([firstTime, lastTime])
                .range([0, width]);

            const y = isFreq ? 
                d3.scaleLinear()
                    .domain([0, 384])  // Frequency range in kHz
                    .range([height, 0]) :
                d3.scaleLinear()
                    .domain([0, 1])
                    .range([height, 0]);

            // Create zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.5, 20])
                .extent([[0, 0], [width, height]])
                .on("zoom", (event) => {{
                    const newX = event.transform.rescaleX(x);
                    const newY = event.transform.rescaleY(y);
                    svg.select(".x-axis").call(xAxis.scale(newX));
                    svg.select(".y-axis").call(yAxis.scale(newY));
                    if (isFreq) {{
                        svg.selectAll("line")
                            .attr("x1", d => newX(new Date(d.timestamp)))
                            .attr("x2", d => newX(new Date(d.timestamp)))
                            .attr("y1", d => newY(d.high_freq))
                            .attr("y2", d => newY(d.low_freq));
                    }} else {{
                        svg.selectAll("circle")
                            .attr("cx", d => newX(new Date(d.timestamp)))
                            .attr("cy", d => newY(isSpeciesProb ? d.class_prob : d.det_prob));
                    }}
                }});

            // Add zoom behavior to SVG
            svg.call(zoom);

            // Create axes
            const xAxis = d3.axisBottom(x)
                .ticks(width / 80)
                .tickFormat(d3.timeFormat("%Y-%m-%d %H:%M"));

            const yAxis = d3.axisLeft(y)
                .ticks(isFreq ? 16 : 5)  // 16 ticks for frequency (384/25 + 1)
                .tickFormat(d => isFreq ? d + " kHz" : d * 100 + "%");

            // Add axes
            svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${{height}})`)
                .call(xAxis)
                .selectAll("text")
                .attr("transform", "rotate(-45)")
                .style("text-anchor", "end");

            svg.append("g")
                .attr("class", "y-axis")
                .call(yAxis);

            // Add axis labels
            svg.append("text")
                .attr("text-anchor", "middle")
                .attr("transform", `translate(${{-margin.left/2 - 15}},${{height/2}}) rotate(-90)`)
                .text(isFreq ? "Frequency (kHz)" : (isSpeciesProb ? "Species Probability" : "Detection Probability"));

            svg.append("text")
                .attr("text-anchor", "middle")
                .attr("transform", `translate(${{width/2}},${{height + margin.bottom - 5}})`)
                .text("Time");

            // Create tooltip
            const tooltip = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0)
                .style("position", "absolute")
                .style("background-color", "white")
                .style("border", "1px solid #ddd")
                .style("padding", "10px")
                .style("border-radius", "5px")
                .style("pointer-events", "none");

            // Add points
            if (isFreq) {{
                // For frequency chart, use lines
                const freqData = data.timestamps.map((t, i) => {{
                    const high_freq = data.high_freqs[i];
                    const low_freq = data.low_freqs[i];
                    if (high_freq === undefined || low_freq === undefined) {{
                        return null;
                    }}
                    if (high_freq < 0 || low_freq < 0) {{
                        return null;
                    }}
                    if (high_freq < low_freq) {{
                        return null;
                    }}
                    return {{
                        timestamp: t,
                        species: data.species[i],
                        det_prob: data.det_probs[i],
                        class_prob: data.class_probs[i],
                        high_freq: high_freq / 1000,  // Convert to kHz
                        low_freq: low_freq / 1000,   // Convert to kHz
                        common_name: speciesNames[data.species[i]] || ''
                    }};
                }}).filter(d => d !== null);  // Remove any null entries

                // Sort data by timestamp to ensure proper ordering
                freqData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

                // Create a group for all lines
                const lineGroup = svg.append("g")
                    .attr("class", "frequency-lines");

                // Add lines for each detection
                lineGroup.selectAll("line")
                    .data(freqData)
                    .enter()
                    .append("line")
                    .attr("x1", d => x(new Date(d.timestamp)))
                    .attr("x2", d => x(new Date(d.timestamp)))
                    .attr("y1", d => y(d.high_freq))
                    .attr("y2", d => y(d.low_freq))
                    .attr("stroke", d => speciesColors[d.species])
                    .attr("stroke-width", 2)
                    .on("mouseover", function(event, d) {{
                        tooltip.transition()
                            .duration(200)
                            .style("opacity", .9);
                        tooltip.html(`Species: ${{d.species}}<br/>Common Name: ${{d.common_name || 'Unknown'}}<br/>Detection Probability: ${{(d.det_prob * 100).toFixed(1)}}%<br/>Species Probability: ${{(d.class_prob * 100).toFixed(1)}}%<br/>Frequency Range: ${{d.low_freq.toFixed(1)}} - ${{d.high_freq.toFixed(1)}} kHz<br/>Time: ${{d.timestamp}}`)
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                    }})
                    .on("mouseout", function(d) {{
                        tooltip.transition()
                            .duration(500)
                            .style("opacity", 0);
                    }});

                // Update zoom behavior to handle the line group
                zoom.on("zoom", (event) => {{
                    const newX = event.transform.rescaleX(x);
                    const newY = event.transform.rescaleY(y);
                    svg.select(".x-axis").call(xAxis.scale(newX));
                    svg.select(".y-axis").call(yAxis.scale(newY));
                    lineGroup.selectAll("line")
                        .attr("x1", d => newX(new Date(d.timestamp)))
                        .attr("x2", d => newX(new Date(d.timestamp)))
                        .attr("y1", d => newY(d.high_freq))
                        .attr("y2", d => newY(d.low_freq));
                }});
            }} else {{
                // For probability charts, use circles
                svg.selectAll("circle")
                    .data(data.timestamps.map((t, i) => ({{
                        timestamp: t,
                        species: data.species[i],
                        det_prob: data.det_probs[i],
                        class_prob: data.class_probs[i],
                        common_name: speciesNames[data.species[i]] || ''
                    }})))
                    .enter()
                    .append("circle")
                    .attr("cx", d => x(new Date(d.timestamp)))
                    .attr("cy", d => y(isSpeciesProb ? d.class_prob : d.det_prob))
                    .attr("r", 4)
                    .style("fill", d => isSpeciesProb ? speciesColors[d.species] : "rgba(54, 162, 235, 0.7)")
                    .on("mouseover", function(event, d) {{
                        tooltip.transition()
                            .duration(200)
                            .style("opacity", .9);
                        tooltip.html(`Species: ${{d.species}}<br/>Common Name: ${{d.common_name || 'Unknown'}}<br/>Detection Probability: ${{(d.det_prob * 100).toFixed(1)}}%<br/>Species Probability: ${{(d.class_prob * 100).toFixed(1)}}%<br/>Time: ${{d.timestamp}}`)
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                    }})
                    .on("mouseout", function(d) {{
                        tooltip.transition()
                            .duration(500)
                            .style("opacity", 0);
                    }});
            }}

            // Add legend for species probability or frequency chart
            if (isSpeciesProb || isFreq) {{
                const legendDiv = document.getElementById(isFreq ? 'freqTimeLegend' : 'speciesTimeLegend');
                // Get unique species in order of appearance
                const uniqueSpecies = Array.from(new Set(data.species));
                uniqueSpecies.forEach(species => {{
                    const color = speciesColors[species];
                    const label = speciesNames[species] ? `${{species}} (${{speciesNames[species]}})` : species;
                    const item = document.createElement('div');
                    item.className = 'legend-item';
                    item.innerHTML = `<span class="legend-color" style="background:${{color}}"></span>${{label}}`;
                    legendDiv.appendChild(item);
                }});
            }}
        }}

        function filterData(minDetProb, minClassProb) {{
            const filteredData = {{
                timestamps: [],
                species: [],
                det_probs: [],
                class_probs: [],
                hours: new Array(24).fill(0),
                high_freqs: [],
                low_freqs: []
            }};

            // Get selected date range
            const dateRange = document.getElementById('dateRange')._flatpickr.selectedDates;
            const startDate = dateRange[0];
            const endDate = dateRange[1];

            // First collect all detections that meet both probability thresholds and date range
            const validDetections = [];
            for (let i = 0; i < originalData.timestamps.length; i++) {{
                const timestamp = new Date(originalData.timestamps[i]);
                if (originalData.det_probs[i] >= minDetProb && 
                    originalData.class_probs[i] >= minClassProb &&
                    timestamp >= startDate && 
                    timestamp <= endDate) {{
                    validDetections.push({{
                        timestamp: originalData.timestamps[i],
                        species: originalData.species[i],
                        det_prob: originalData.det_probs[i],
                        class_prob: originalData.class_probs[i],
                        high_freq: originalData.high_freqs[i],
                        low_freq: originalData.low_freqs[i]
                    }});
                }}
            }}

            // Then process the valid detections
            validDetections.forEach(detection => {{
                filteredData.timestamps.push(detection.timestamp);
                filteredData.species.push(detection.species);
                filteredData.det_probs.push(detection.det_prob);
                filteredData.class_probs.push(detection.class_prob);
                filteredData.high_freqs.push(detection.high_freq);
                filteredData.low_freqs.push(detection.low_freq);
                
                const dt = new Date(detection.timestamp);
                filteredData.hours[dt.getHours()]++;
            }});

            // Convert species array to count object
            const speciesCounts = filteredData.species.reduce((acc, species) => {{
                acc[species] = (acc[species] || 0) + 1;
                return acc;
            }}, {{}});

            return {{
                ...filteredData,
                speciesCounts: speciesCounts
            }};
        }}

        function createFreqDistChart(highFreqs, lowFreqs) {{
            // Define binning
            const minFreq = 0;
            const maxFreq = 384;
            const binSize = 5;
            const numBins = Math.ceil((maxFreq - minFreq) / binSize);
            const freqBins = Array(numBins).fill(0);

            // Combine and bin all frequencies (convert Hz to kHz)
            [...highFreqs, ...lowFreqs].forEach(f => {{
                const f_khz = f / 1000;
                if (f_khz >= minFreq && f_khz <= maxFreq) {{
                    const bin = Math.floor((f_khz - minFreq) / binSize);
                    freqBins[bin]++;
                }}
            }});

            // Bin labels
            const binLabels = Array.from({{length: numBins}}, (_, i) => `${{minFreq + i*binSize}}-${{minFreq + (i+1)*binSize}} kHz`);

            // Create or update chart
            if (freqDistChart) freqDistChart.destroy();
            freqDistChart = new Chart(document.getElementById('freqDistChart'), {{
                type: 'bar',
                data: {{
                    labels: binLabels,
                    datasets: [{{
                        label: 'Frequency Distribution',
                        data: freqBins,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ position: 'top' }},
                        title: {{ display: true, text: 'Frequency Distribution (kHz)' }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{ display: true, text: 'Count' }}
                        }},
                        x: {{
                            title: {{ display: true, text: 'Frequency Range (kHz)' }}
                        }}
                    }}
                }}
            }});
        }}

        function updateCharts() {{
            // Show loading cursor
            document.body.style.cursor = 'wait';
            
            const [minDetProb, minClassProb] = document.getElementById('probFilter').value.split(',').map(Number);
            const filteredData = filterData(minDetProb, minClassProb);

            // Update time charts
            createTimeChart(filteredData, false);  // Detection probability chart
            createTimeChart(filteredData, true);   // Species probability chart
            createTimeChart(filteredData, false, true);  // Frequency chart

            // Update species chart
            createSpeciesChart(filteredData.speciesCounts);

            // Update probability charts
            const detProbBins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            const classProbBins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            
            originalData.det_probs.forEach(p => {{
                if (p < 0.1) detProbBins[0]++;
                else if (p < 0.2) detProbBins[1]++;
                else if (p < 0.3) detProbBins[2]++;
                else if (p < 0.4) detProbBins[3]++;
                else if (p < 0.5) detProbBins[4]++;
                else if (p < 0.6) detProbBins[5]++;
                else if (p < 0.7) detProbBins[6]++;
                else if (p < 0.8) detProbBins[7]++;
                else if (p < 0.9) detProbBins[8]++;
                else detProbBins[9]++;
            }});
            
            originalData.class_probs.forEach(p => {{
                if (p < 0.1) classProbBins[0]++;
                else if (p < 0.2) classProbBins[1]++;
                else if (p < 0.3) classProbBins[2]++;
                else if (p < 0.4) classProbBins[3]++;
                else if (p < 0.5) classProbBins[4]++;
                else if (p < 0.6) classProbBins[5]++;
                else if (p < 0.7) classProbBins[6]++;
                else if (p < 0.8) classProbBins[7]++;
                else if (p < 0.9) classProbBins[8]++;
                else classProbBins[9]++;
            }});
            
            probChart.data.datasets[0].data = detProbBins;
            probChart.data.datasets[1].data = classProbBins;
            probChart.update();

            // Update hour chart
            hourChart.data.datasets[0].data = filteredData.hours;
            hourChart.update();

            // Update species by hour chart
            const speciesByHour = Array(24).fill().map(() => ({{}}));
            for (let i = 0; i < filteredData.timestamps.length; i++) {{
                const hour = new Date(filteredData.timestamps[i]).getHours();
                const species = filteredData.species[i];
                speciesByHour[hour][species] = (speciesByHour[hour][species] || 0) + 1;
            }}

            // Get all unique species
            const allSpecies = [...new Set(filteredData.species)];
            
            // Update datasets
            speciesHourChart.data.datasets = allSpecies.map(species => ({{
                label: speciesNames[species] ? `${{species}} (${{speciesNames[species]}})` : species,
                data: speciesByHour.map(hourData => hourData[species] || 0),
                backgroundColor: speciesColors[species]
            }}));
            speciesHourChart.update();

            createFreqDistChart(filteredData.high_freqs, filteredData.low_freqs);

            // Reset cursor after all updates are complete
            document.body.style.cursor = 'default';
        }}

        // Initialize charts
        document.addEventListener('DOMContentLoaded', function() {{
            // Initial time charts
            createTimeChart(originalData, false);  // Detection probability chart
            createTimeChart(originalData, true);   // Species probability chart
            createTimeChart(originalData, false, true);  // Frequency chart

            // Initial species chart
            createSpeciesChart({json.dumps(species)});

            // Combined probability distribution chart
            probChart = new Chart(document.getElementById('probChart'), {{
                type: 'bar',
                data: {{
                    labels: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'],
                    datasets: [
                        {{
                            label: 'Detection Probability',
                            data: {json.dumps([
                                sum(1 for p in det_probs if 0 <= p < 0.1),
                                sum(1 for p in det_probs if 0.1 <= p < 0.2),
                                sum(1 for p in det_probs if 0.2 <= p < 0.3),
                                sum(1 for p in det_probs if 0.3 <= p < 0.4),
                                sum(1 for p in det_probs if 0.4 <= p < 0.5),
                                sum(1 for p in det_probs if 0.5 <= p < 0.6),
                                sum(1 for p in det_probs if 0.6 <= p < 0.7),
                                sum(1 for p in det_probs if 0.7 <= p < 0.8),
                                sum(1 for p in det_probs if 0.8 <= p < 0.9),
                                sum(1 for p in det_probs if 0.9 <= p <= 1.0)
                            ])},
                            backgroundColor: 'rgba(75, 192, 192, 0.7)'
                        }},
                        {{
                            label: 'Species Probability',
                            data: {json.dumps([
                                sum(1 for p in class_probs if 0 <= p < 0.1),
                                sum(1 for p in class_probs if 0.1 <= p < 0.2),
                                sum(1 for p in class_probs if 0.2 <= p < 0.3),
                                sum(1 for p in class_probs if 0.3 <= p < 0.4),
                                sum(1 for p in class_probs if 0.4 <= p < 0.5),
                                sum(1 for p in class_probs if 0.5 <= p < 0.6),
                                sum(1 for p in class_probs if 0.6 <= p < 0.7),
                                sum(1 for p in class_probs if 0.7 <= p < 0.8),
                                sum(1 for p in class_probs if 0.8 <= p < 0.9),
                                sum(1 for p in class_probs if 0.9 <= p <= 1.0)
                            ])},
                            backgroundColor: 'rgba(153, 102, 255, 0.7)'
                        }}
                    ]
                }},
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: 'Number of Detections'
                            }}
                        }},
                        x: {{
                            title: {{
                                display: true,
                                text: 'Probability Range'
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'top'
                        }}
                    }}
                }}
            }});

            // Hour of day chart
            hourChart = new Chart(document.getElementById('hourChart'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps([f'{h:02d}:00' for h in range(24)])},
                    datasets: [{{
                        label: 'Number of Detections',
                        data: {json.dumps(hours)},
                        backgroundColor: 'rgba(153, 102, 255, 0.7)'
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: 'Number of Detections'
                            }}
                        }},
                        x: {{
                            title: {{
                                display: true,
                                text: 'Hour of Day'
                            }}
                        }}
                    }}
                }}
            }});

            // Species by hour chart
            const speciesByHour = Array(24).fill().map(() => ({{}}));
            for (let i = 0; i < originalData.timestamps.length; i++) {{
                const hour = new Date(originalData.timestamps[i]).getHours();
                const species = originalData.species[i];
                speciesByHour[hour][species] = (speciesByHour[hour][species] || 0) + 1;
            }}

            // Get all unique species
            const allSpecies = [...new Set(originalData.species)];
            
            speciesHourChart = new Chart(document.getElementById('speciesHourChart'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps([f'{h:02d}:00' for h in range(24)])},
                    datasets: allSpecies.map(species => ({{
                        label: speciesNames[species] ? `${{species}} (${{speciesNames[species]}})` : species,
                        data: speciesByHour.map(hourData => hourData[species] || 0),
                        backgroundColor: speciesColors[species]
                    }}))
                }},
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            stacked: true,
                            title: {{
                                display: true,
                                text: 'Number of Detections'
                            }}
                        }},
                        x: {{
                            stacked: true,
                            title: {{
                                display: true,
                                text: 'Hour of Day'
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{
                                boxWidth: 12,
                                padding: 10
                            }}
                        }}
                    }}
                }}
            }});

            createFreqDistChart(originalData.high_freqs, originalData.low_freqs);
        }});
    </script>
</body>
</html>
'''

    # Write the HTML file
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"Created visualization in {output_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create HTML visualization of bat detection data')
    parser.add_argument('input_file', help='Input JSON file with bat detections')
    parser.add_argument('--output', '-o', default='bat_detections.html',
                      help='Output HTML file (default: bat_detections.html)')
    parser.add_argument('--version', '-v', action='version',
                      version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} not found")
        return
    
    data = load_data(args.input_file)
    create_html_visualization(data, args.output)

if __name__ == "__main__":
    main() 