import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {TimeControllerDomainComponent} from './time-controller-domain.component';
import {AppComponent} from '../app.component';


const routes: Routes = [
  {
    path: '',
    component: AppComponent,
    children: [
      { path: '', component: TimeControllerDomainComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TimeControllerDomainRoutingModule { }
