import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { NgForm } from '@angular/forms';
import { CarPreference } from 'icare-frontend-openapi';
import { CheckboxItem, DropdownItem } from './filter.interface';

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.css'],
})
export class FilterComponent implements OnInit {
  @Output() filterFormSubmitEvent = new EventEmitter<CarPreference>()
  brandArr: CheckboxItem[] = [
    {id:'Honda', isSelected: true},
    {id:'Hyundai', isSelected: false},
    {id:'Kia', isSelected: false},
    {id:'Mazda', isSelected: false},
    {id:'Toyota', isSelected: false}
  ];
  typeArr: CheckboxItem[] = [
    {id:'Hatchback', isSelected: true},
    {id:'MPV', isSelected: false},
    {id:'Sedan', isSelected: false},
    {id:'SUV', isSelected: false}
  ];
  yearArr: DropdownItem[] = [{id: '2022', description: '2022'}, {id: '2023', description: '2023'}, {id: '2024', description: '2024'}];
  monthArr: DropdownItem[] = [
    {id: '01', description: 'Jan'}, {id: '02', description: 'Feb'}, {id: '03', description: 'Mar'}, {id: '04', description: 'Apr'},
    {id: '05', description: 'May'}, {id: '06', description: 'Jun'}, {id: '07', description: 'Jul'}, {id:'08', description: 'Aug'},
    {id: '09', description: 'Sep'}, {id: '10', description: 'Oct'}, {id: '11', description: 'Nov'}, {id: '12', description: 'Dec'}
  ];
  startYear: string = '2022'
  startMonth: string = 'Nov'
  endYear: string = '2022'
  endMonth: string = 'Nov'
  showBrandError: boolean = false
  showTypeError: boolean = false
  budgetAmt: number = 150000


  constructor() { }

  ngOnInit(): void {
    let now = this.getLocalDate(new Date())
    this.startYear = now[0]
    this.endYear = now[0]
    let mth: any = this.monthArr.find(x => x.id === now[1])
    if(mth){
      this.startMonth = mth.description
      this.endMonth = mth.description
    }
    this.submitInitialValues()
  }

  brandCheckChange(e: any){
    if(!e){
      this.showBrandError = !this.isRequiredcheckboxListValid(this.brandArr)
    } else {
      this.showBrandError = false
    }
  }

  typeCheckChange(e: any){
    if(!e){
      this.showTypeError = !this.isRequiredcheckboxListValid(this.typeArr)
    } else {
      this.showTypeError = false
    }
  }

  isRequiredcheckboxListValid(checkboxArr: CheckboxItem[]){
    let selected = checkboxArr.filter(x => x.isSelected === true)
    if(selected.length > 0){
      return true
    }
    return false
  }

  convertSelectedcheckboxToStrArr(checkboxArr: CheckboxItem[]){
    let strArr: string[] = []
    let selected = checkboxArr.filter(x => x.isSelected === true)
    selected.forEach(x => {
      strArr.push(x.id)
    })
    return strArr
  }

  getLocalDate(date: Date){
    let localDt = date.toLocaleString('en-GB', {
      timeZone: 'Asia/Singapore'
    });
    let splittedDt = localDt.split(', ')
    let datePart = splittedDt[0].split('/')
    // [year, month, day]
    return [datePart[2], datePart[1], datePart[0]]
  }

  submitInitialValues(){
    let brand: string[] = this.convertSelectedcheckboxToStrArr(this.brandArr)
    let type: string[] = this.convertSelectedcheckboxToStrArr(this.typeArr)
    let carPreference: CarPreference = {
      budget: this.budgetAmt,
      startYear: this.startYear,
      startMonth: this.startMonth,
      endYear: this.endYear,
      endMonth: this.endMonth,
      brand: brand,
      type: type
    }
    this.filterFormSubmitEvent.emit(carPreference)
  }

  onSubmit(form: NgForm){
    console.log(form.value)
    let isTypeValid: boolean = this.isRequiredcheckboxListValid(this.typeArr)
    let isBrandValid: boolean = this.isRequiredcheckboxListValid(this.brandArr)
    if(!isTypeValid || !isBrandValid){
      if(!isTypeValid) this.showTypeError = true
      if(!isBrandValid) this.showBrandError = true
      return
    }
    let brand: string[] = this.convertSelectedcheckboxToStrArr(this.brandArr)
    let type: string[] = this.convertSelectedcheckboxToStrArr(this.typeArr)
    let carPreference: CarPreference = {
      budget: form.value.budget,
      startYear: form.value.startYear,
      startMonth: form.value.startMonth,
      endYear: form.value.endYear,
      endMonth: form.value.endMonth,
      brand: brand,
      type: type
    }
    this.filterFormSubmitEvent.emit(carPreference)
  }
}
