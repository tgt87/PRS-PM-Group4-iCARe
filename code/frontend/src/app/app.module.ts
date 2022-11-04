import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { environment } from '../environments/environment';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { ApiModule, BASE_PATH } from 'icare-frontend-openapi';
import { DashboardComponent } from './dashboard/dashboard/dashboard.component';
import { CoeGraphComponent } from './dashboard/coe-graph/coe-graph.component';
import { CarListComponent } from './dashboard/car-list/car-list.component';
import { FilterComponent } from './dashboard/filter/filter.component';


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    CoeGraphComponent,
    CarListComponent,
    FilterComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ApiModule,
    NgbModule,
    NgxChartsModule
  ],
  providers: [{
    provide: BASE_PATH, useValue: environment.basePath
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
