import { Component, Input, OnInit } from '@angular/core';
import { Car } from 'icare-frontend-openapi';

@Component({
  selector: 'app-car-list',
  templateUrl: './car-list.component.html',
  styleUrls: ['./car-list.component.css']
})
export class CarListComponent implements OnInit {
  @Input() cars: Car[] = []
  carsArr: Car[] = []
  paginatedCarArr: Car[] = []
  showPrev: boolean = false
  showNext: boolean = true
  showRecords: number = 4
  startIdx: number = 0
  endIdx: number = 0
  carsArrLength: number = 0

  constructor() { 
    
  }

  ngOnInit() {
    this.carsArr = this.cars;
    this.carsArrLength = this.carsArr.length
    if(this.carsArrLength === this.showRecords){
      this.paginatedCarArr = this.carsArr
      this.endIdx = this.showRecords
    } else {
      this.endIdx = this.carsArrLength < this.showRecords ? this.carsArrLength : this.showRecords
      this.paginatedCarArr = this.carsArr.slice(this.startIdx, this.endIdx)
      this.showNext = this.carsArrLength > this.showRecords
    }
  }


  showNextClick(){
    this.startIdx = this.startIdx + this.showRecords
    if(this.endIdx + this.showRecords > this.carsArrLength){
      this.endIdx = this.carsArrLength
    } else {
      this.endIdx = this.endIdx + this.showRecords
    }
    this.paginatedCarArr = this.carsArr.slice(this.startIdx, this.endIdx)
    this.showPrev = true
    if(this.endIdx >= this.carsArrLength){
      this.showNext = false
    }
  }

  showPrevClick(){
    if(this.startIdx - this.showRecords < 0){
      this.startIdx = 0
    } else {
      this.startIdx = this.startIdx - this.showRecords
    }
    this.endIdx = this.startIdx + this.showRecords
    this.paginatedCarArr = this.carsArr.slice(this.startIdx, this.endIdx)
    this.showNext = true
    if(this.startIdx === 0){
      this.showPrev = false
    }
  }

}
