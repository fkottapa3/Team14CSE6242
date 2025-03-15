// Fetch tenant data from the backend
fetch("http://127.0.0.1:5000/api/tenants")
	.then((response) => response.json())
	.then((data) => {
		const loadingMessage =
			document.getElementById("loading-message");
		if (loadingMessage) {
			loadingMessage.remove(); // Remove loading message only if it exists
		}
		console.log("Tenant Data:", data);
		createBarChart(data);
		createPieChart(data);
		createMonthlyBarChart(data); // New bar chart for monthly joins
	})
	.catch((error) => {
		console.error("Error fetching tenant data:", error);
		const loadingMessage =
			document.getElementById("loading-message");
		if (loadingMessage) {
			loadingMessage.textContent =
				"Failed to load data. Please try again later.";
		}
	});

// Create a bar chart for tenant rents
function createBarChart(data) {
	const margin = { top: 20, right: 30, bottom: 40, left: 50 };
	const width = 600 - margin.left - margin.right;
	const height = 400 - margin.top - margin.bottom;

	const svg = d3
		.select("#bar-chart")
		.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", `translate(${margin.left},${margin.top})`);

	const x = d3
		.scaleBand()
		.domain(data.map((d) => d.tenant_name)) // Fixed key name
		.range([0, width])
		.padding(0.1);

	const y = d3
		.scaleLinear()
		.domain([0, d3.max(data, (d) => d.agreed_rent)])
		.range([height, 0]);

	svg.append("g")
		.selectAll("rect")
		.data(data)
		.enter()
		.append("rect")
		.attr("x", (d) => x(d.tenant_name))
		.attr("y", (d) => y(d.agreed_rent))
		.attr("width", x.bandwidth())
		.attr("height", (d) => height - y(d.agreed_rent))
		.attr("fill", "steelblue");

	svg.append("g")
		.attr("transform", `translate(0,${height})`)
		.call(d3.axisBottom(x));

	svg.append("g").call(d3.axisLeft(y));
}

function createPieChart(data) {
	const width = 400,
		height = 400,
		radius = Math.min(width, height) / 2;

	const svg = d3
		.select("#pie-chart")
		.append("svg")
		.attr("width", width)
		.attr("height", height)
		.append("g")
		.attr("transform", `translate(${width / 2},${height / 2})`);

	const pie = d3.pie().value((d) => d.admission_fee);

	const arc = d3.arc().innerRadius(0).outerRadius(radius);

	const color = d3.scaleOrdinal(d3.schemeCategory10);

	const arcs = svg.selectAll("arc").data(pie(data)).enter().append("g");

	arcs.append("path")
		.attr("d", arc)
		.attr("fill", (d, i) => color(i));

	arcs.append("text")
		.attr("transform", (d) => `translate(${arc.centroid(d)})`)
		.attr("text-anchor", "middle")
		.text((d) => d.data.tenant_name);
}

function createMonthlyBarChart(data) {
	const margin = { top: 20, right: 30, bottom: 50, left: 50 };
	const width = 600 - margin.left - margin.right;
	const height = 400 - margin.top - margin.bottom;

	const svg = d3
		.select("#monthly-join-chart")
		.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", `translate(${margin.left},${margin.top})`);

	console.log(
		"Join Dates in Data:",
		data.map((d) => d.join_date)
	);

	// Parse dates and extract month
	const parseDate = d3.timeParse("%Y-%m-%d");
	data.forEach((d) => {
		d.join_date = parseDate(d.join_date); // Parse join_date
		d.month = d.join_date ? d.join_date.getMonth() : null; // Extract month
	});

	console.log("Parsed Data with Month:", data); // Debugging log

	// Group by month and count
	const monthCounts = d3.rollup(
		data.filter((d) => d.month !== null),
		(v) => v.length,
		(d) => d.month
	);

	console.log("Month Counts:", monthCounts); // Debugging log

	const monthData = Array.from(monthCounts, ([month, count]) => ({
		month,
		count,
	}));

	console.log("Formatted Month Data:", monthData); // Debugging log

	// Month names for x-axis labels
	const monthNames = [
		"January",
		"February",
		"March",
		"April",
		"May",
		"June",
		"July",
		"August",
		"September",
		"October",
		"November",
		"December",
	];

	const x = d3
		.scaleBand()
		.domain(monthNames)
		.range([0, width])
		.padding(0.1);

	const y = d3
		.scaleLinear()
		.domain([0, d3.max(monthData, (d) => d.count)])
		.range([height, 0]);

	// Draw bars
	svg.append("g")
		.selectAll("rect")
		.data(monthData)
		.enter()
		.append("rect")
		.attr("x", (d) => x(monthNames[d.month]))
		.attr("y", (d) => y(d.count))
		.attr("width", x.bandwidth())
		.attr("height", (d) => height - y(d.count))
		.attr("fill", "steelblue");

	// Add axes
	svg.append("g")
		.attr("transform", `translate(0,${height})`)
		.call(d3.axisBottom(x))
		.selectAll("text")
		.attr("transform", "rotate(-45)")
		.style("text-anchor", "end");

	svg.append("g").call(d3.axisLeft(y));
}
