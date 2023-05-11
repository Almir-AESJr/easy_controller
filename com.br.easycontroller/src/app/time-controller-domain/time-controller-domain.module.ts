import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TimeControllerDomainComponent} from './time-controller-domain.component';
import {TimeControllerDomainRoutingModule} from './time-controller-domain-routing.module';
import {MatExpansionModule} from '@angular/material/expansion';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";
import {TimeControllerDomainService} from './time-controller-domain.service';
import { PlotlyModule } from 'angular-plotly.js';
import * as PlotlyJS from 'plotly.js-dist-min';
import { NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { NgbDropdownModule} from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { ClipboardModule } from '@angular/cdk/clipboard';
import { DecimalNumberDirective } from '../onlyDecimal.directive';

PlotlyModule.plotlyjs = PlotlyJS;

@NgModule({
  declarations: [TimeControllerDomainComponent, DecimalNumberDirective],
  imports: [
    FormsModule,
    MatExpansionModule,
    CommonModule,
    TimeControllerDomainRoutingModule,
    MatInputModule,
    MatButtonModule,
    PlotlyModule,
    NgbModule,
    NgbDropdownModule,
    HttpClientModule,
    ClipboardModule,
  ],
  providers: [TimeControllerDomainService],
})
export class TimeControllerDomainModule {}
