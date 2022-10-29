const svg = d3.select('#basic-demo svg');

svg
  .selectAll('rect')
  .data([50, 100, 200, 100, 50])
  .enter()
  .append('rect')
  .attr('y', (num, idx) => idx * 40)
  .attr('x', 0)
  .attr('width', (num) => num)
  .attr('height', 30)
  .attr('fill', (num, idx) => d3.hsl(idx * 30, 1.0, 0.8));