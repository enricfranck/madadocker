import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AventureComponent } from './aventure.component';

describe('AventureComponent', () => {
  let component: AventureComponent;
  let fixture: ComponentFixture<AventureComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AventureComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AventureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
