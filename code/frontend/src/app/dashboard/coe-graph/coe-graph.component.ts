import { Component, OnInit, Input } from '@angular/core';
import { LegendPosition } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-coe-graph',
  templateUrl: './coe-graph.component.html',
  styleUrls: ['./coe-graph.component.css']
})
export class CoeGraphComponent implements OnInit {
  @Input() coeResults: any[] = [];

  // graph options
  options = {
    legend: true,
    legendPosition: LegendPosition.Right,
    xAxis: true,
    yAxis: true,
    showYAxisLabel: true,
    showXAxisLabel: true,
    showGridLines: true,
    timeline: true,
    xAxisLabel: 'Bidding Exercises',
    yAxisLabel: 'COE Prices ($)',
  }
  
  constructor() {}

  ngOnInit(): void {
  }

  onSelect(data: any): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }


}
