import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { CoeService, CarPreference, Car, CarService } from 'icare-frontend-openapi';
import { DropdownItem } from '../filter/filter.interface';
import { FormatterService } from 'src/app/services/formatter.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  subscription: Subscription = new Subscription()
  cars: Car[] = []
  coeResults: any[] = []

  coeCategoryArr: DropdownItem[] = [
    {id: 'A', description: 'Category A'}, {id: 'B', description: 'Category B'}, {id: 'C', description: 'Category C'},
    {id: 'D', description: 'Category D'}, {id: 'E', description: 'Category E'}
  ]
  selectedCoeCategory: string = 'A'      
  isCoeDataLoaded: boolean = false            
  isCarDataLoaded: boolean = false

  constructor(private coeService: CoeService, private carService: CarService, private formatterService: FormatterService) { }

  ngOnInit() {
    this.isCoeDataLoaded = false
    let subscription1 = this.coeService.getCoePredictionByCategory(this.selectedCoeCategory)
                                      .subscribe({
                                        next: result => {
                                          this.coeResults = this.formatterService.formatArrayObjectKey(result)
                                          this.isCoeDataLoaded = true
                                        }, 
                                        error: e => console.log(e)
                                      })
    this.subscription.add(subscription1)
  }

  filterFormSubmitEvent(carPreference: CarPreference){
    this.isCarDataLoaded = false
    let subscription2 = this.carService.suggestCarsByUserPreference(carPreference)
                                      .subscribe({
                                        next: result => {
                                          this.cars = this.formatterService.formatArrayObjectKey(result)
                                          this.isCarDataLoaded = true
                                        }, 
                                        error: e => console.log(e)
                                      })
    this.subscription.add(subscription2)
  }

  ngOnDestroy() {
    if(this.subscription) this.subscription.unsubscribe()
  }

}
