import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CoeGraphComponent } from './coe-graph.component';

describe('CoeGraphComponent', () => {
  let component: CoeGraphComponent;
  let fixture: ComponentFixture<CoeGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CoeGraphComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CoeGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
