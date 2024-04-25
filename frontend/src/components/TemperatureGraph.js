import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const TemperatureGraph = ({ data, variable }) => {
    const d3Container = useRef(null);

    useEffect(() => {
        if (data && d3Container.current) {
            const svg = d3.select(d3Container.current);
            svg.selectAll('*').remove();

            const margin = { top: 20, right: 20, bottom: 30, left: 50 };
            const width = 960 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const x = d3.scaleTime()
                .domain(d3.extent(data, d => new Date(d.time)))
                .range([0, width]);

            const y = d3.scaleLinear()
                .domain([d3.min(data, d => d[variable]) - 1, d3.max(data, d => d[variable]) + 1])
                .range([height, 0]);

            const line = d3.line()
                .x(d => x(new Date(d.time)))
                .y(d => y(d[variable]))
                .curve(d3.curveMonotoneX);

            const mainSvg = svg.append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            mainSvg.append('g')
                .attr('transform', `translate(0,${height})`)
                .call(d3.axisBottom(x));

            mainSvg.append('g')
                .call(d3.axisLeft(y));

            mainSvg.append('path')
                .datum(data)
                .attr('fill', 'none')
                .attr('stroke', 'steelblue')
                .attr('stroke-width', 3)
                .attr('d', line);
        }
    }, [data, variable]);

    return (
        <svg
            ref={d3Container}
            width={960}
            height={500}
            style={{ maxWidth: '100%', height: 'auto', border: '1px solid black' }}
        />
    );
};

export default TemperatureGraph;