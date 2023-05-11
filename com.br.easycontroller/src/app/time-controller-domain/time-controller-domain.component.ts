import { HttpClient, HttpResponse } from '@angular/common/http';
import {Component, OnInit, ViewEncapsulation, Input, forwardRef} from '@angular/core';
import {Matriz} from "./Matriz";
import {TimeControllerDomainService} from "./time-controller-domain.service";
import Swal from 'sweetalert2';
import {NG_VALUE_ACCESSOR, NG_VALIDATORS, Validator, FormControl, ValidationErrors,ControlValueAccessor} from '@angular/forms';

@Component({
  templateUrl: './time-controller-domain.component.html',
  styleUrls: ['./time-controller-domain.component.css'],
  encapsulation: ViewEncapsulation.None,
  selector: 'numeric-input',
  providers: [
    // {
    //   provide: NG_VALUE_ACCESSOR,
    //   useExisting: forwardRef(() => NumericInputComponent),
    //   multi: true,
    // },
    // {
    //   provide: NG_VALIDATORS,
    //   useExisting: forwardRef(() => NumericInputComponent),
    //   multi: true,
    // },
  ],
})
export class TimeControllerDomainComponent implements OnInit {
  Nstates: number = 1;
  quadN: number = 2;
  inL: number = 1;
  outM: number = 1;
  matrizes: Matriz[] = [
    new Matriz('A'),
    new Matriz('B'),
    new Matriz('C'),
    // new Matriz('D'),
  ];
  matriz_custo: Matriz[] = [new Matriz('Q'), new Matriz('R')];
  matriz_kalman: Matriz[] = [new Matriz('QN'), new Matriz('RN')];
  initialCond: Matriz[] = [new Matriz('CI')];
  graphData: object[] = [];
  graph = { data: this.graphData, layout: this.layout() };
  graphCI = { data: this.graphData, layout: this.layout_CI() };
  control_rank: string = '';
  obsv_rank: string = '';
  vY: any = [];
  yLQR: any = [];
  yLQI: any = [];
  yLQG: any = [];
  yLQGI: any = [];
  y_lqr: any = [];
  y_lqi: any = [];
  y_lqg: any = [];
  y_lqgi: any = [];
  y_enc: any = [];
  u_enc: any = [];
  uLQR: any = [];
  uLQI: any = [];
  uLQG: any = [];
  uLQGI: any = [];
  u_lqr: any = [];
  u_lqi: any = [];
  u_lqg: any = [];
  u_lqgi: any = [];
  stepMA: any = [];
  panelMA: boolean = false;
  panelCostMatrixLQR: boolean = false;
  panelCostMatrixLQI: boolean = false;
  panelCostMatrixLQG: boolean = false;
  panelCostMatrixLQGI: boolean = false;
  panelCalc_lqr: boolean = false;
  panelCalc_lqi: boolean = false;
  panelCalc_lqg: boolean = false;
  panelCalc_lqgi: boolean = false;
  lineNameIndex: number = 0;
  codes: any = {};
  Nx: number = 0;
  Ny: number = 0;
  Nu: number = 0;
  T: number = 0;
  K: any = [];
  Ki: any = [];
  L: any = [];

  constructor(
    private timeControllerDomainService: TimeControllerDomainService,
    private http: HttpClient
  ) {
    this.createTables();
  }

  ngOnInit(): void {
    console.log('Loading app - time-controller-domain');
  }

  // @Input() public placeHolderText = '';
  // @Input() public isRequired = false;

  // inputValue: string = '';

  // onInputChange(event: any): void {
  //   const newValue = event.target.value;
  //   if (!this.isValidInput(newValue)) {
  //     // Invalid input detected. Resetting to previous value
  //     event.target.value = this.DigitsOnly(event);
  //   } else if (newValue !== this.inputValue) {
  //     // New valid input detected.
  //     this.inputValue = newValue;
  //     // this.propagateChange(this.inputValue);
  //   }
  // }

  // Called for setting the initial value
  // public writeValue(value: string): void {
  //   if (this.isValidInput(value) && this.inputValue !== value) {
  //     this.inputValue = value;
  //   }
  // }

  // // Validates the form, returns null when valid else the validation object
  // public validate(formControl: FormControl): ValidationErrors {
  //   return this.isRequired && !this.inputValue ? { required: true }: null;
  // }

  // Registers function that will be fired when changes are made.
  // public registerOnChange(callbackFunction: (newValue: string) => void): void {
  //   this.propagateChange = callbackFunction;
  // }

  // Non-implemented method which are required by the validator interface
  // public registerOnTouched(callbackFunction: () => void): void {}

  // The method set in registerOnChange to emit changes back to the form
  // private propagateChange = (newValue: string) => {};

  // private isValidInput(value: string): boolean {
  //   // Note: ParseInt is not recommended as it will convert "222aa" -> "222" and assume as valid
  //   return !isNaN(Number(value));
  // }

  // DigitsOnly(event:any) {
  //   event.target.value = 0;
  //     Swal.fire({
  //       position: 'center',
  //       icon: 'warning',
  //       text: 'Entrada inválida!',
  //       showConfirmButton: false,
  //       timer: 1500,
  //     });
  //   }

  createTables() {
    if (this.quadN < 2) {
      this.quadN = 2;
    }
    if (this.inL < 1) {
      this.inL = 1;
    }
    if (this.outM < 1) {
      this.outM = 1;
    }

    for (let i = 0; i < this.matrizes.length; i++) {
      const matriz = this.matrizes[i];
      if (matriz.label === 'A') {
        matriz.lines = this.quadN;
        matriz.cols = this.quadN;
      }
      if (matriz.label === 'B') {
        matriz.lines = this.quadN;
        matriz.cols = this.inL;
      }
      if (matriz.label === 'C') {
        matriz.lines = this.outM;
        matriz.cols = this.quadN;
      }
      // if (matriz.label === 'D') {
      // matriz.lines = this.inL;
      // matriz.cols = this.inL;
      // }
      matriz.values = Array.from(
        Array(matriz.lines),
        () => new Array(matriz.cols)
      );
      for (let i = 0; i < matriz.lines; i++) {
        for (let j = 0; j < matriz.cols; j++) {
          matriz.values[i][j] = 0;
        }
      }
      console.log('matriz.values', matriz.values);
    }
  }

  matrizVaueChange(matryz: any, line: any, col: any, event: any) {
    matryz.values[line][col] = event.target.value;
    console.log('matyz.values', matryz.values);
  }

  trackByFilter(index: number, item: any): number {
    return item.id;
  }

  calc_lqr() {
    this.panelCalc_lqr = true;
    this.panelCalc_lqi = false;
    this.panelCalc_lqg = false;
    this.panelCalc_lqgi = false;
    const matriz_custo_lqr = {
      A: this.matrizes[0].values,
      B: this.matrizes[1].values,
      C: this.matrizes[2].values,
      // D: this.matrizes[3].values,
      Q: this.matriz_custo[0].values,
      R: this.matriz_custo[1].values,
      CI: this.initialCond[0].values,
    };
    console.log('Matriz_custo_lqr:', matriz_custo_lqr);

    this.timeControllerDomainService.calc_lqr(matriz_custo_lqr).then((data) => {
      console.log(data);

      // @ts-ignore
      this.Nx = JSON.parse(data['Nx']);
      // @ts-ignore
      this.Ny = JSON.parse(data['Ny']);
      // @ts-ignore
      this.Nu = JSON.parse(data['Nu']);
      // @ts-ignore
      this.T = JSON.parse(data['T']);
      // @ts-ignore
      this.K = JSON.parse(data['K']);

      this.yLQR = [];
      this.uLQR = [];
      // @ts-ignore
      this.u_enc = data['Uhat'];
      this.u_lqr = JSON.parse(this.u_enc);
      // console.log('X', this.u_lqr);
      // @ts-ignore
      this.y_enc = data['Yout'];
      this.y_lqr = JSON.parse(this.y_enc);
      // console.log('y_enc', this.y_enc);
      // console.log('y_lqr:', this.y_lqr);
      // @ts-ignore
      const vTime = data['time'];
      var dataUlqr = [];

      for (let i = 0; i < this.u_lqr.length; i++) {
        // (this.graph = {
        //   data: [
        //     {
        //       x: vTime,
        //       y: this.u_lqr[i],
        //       mode: 'lines',
        //       connectgaps: true,
        //       marker: { color: 'blue' },
        //     },
        //   ],
        //   layout: this.layout(),
        // }),
        //   this.uLQR.push(this.graph.data);
        // console.log('graph.data_LQR', this.graph.data);
        var datatmpUlqr = {
          x: vTime,
          y: this.u_lqr[i],
          mode: 'lines',
          type: 'scatter',
          connectgaps: true,
          name: `u${i + 1}`,
        };
        dataUlqr.push(datatmpUlqr);
      }

      this.graphCI = {
        data: dataUlqr,
        layout: this.layout_CI(),
      };
      this.uLQR.push(this.graphCI.data);
      console.log('uLQR', this.uLQR);
      console.log('graph.data', this.graphCI.data);

      var dataYlqr = [];

      for (let i = 0; i < this.y_lqr.length; i++) {
        // (this.graph = {
        //   data: [
        //     {
        //       x: vTime,
        //       y: this.y_lqr[i],
        //       mode: 'lines',
        //       connectgaps: true,
        //       marker: { color: 'blue' },
        //     },
        //   ],
        //   layout: this.layout(),
        // }),
        //   this.yLQR.push(this.graph.data),
        //   console.log('graph.data', this.graph.data);

        var datatmpYlqr = {
          x: vTime,
          y: this.y_lqr[i],
          mode: 'lines',
          type: 'scatter',
          connectgaps: true,
          name: `y${i + 1}`,
        };
        dataYlqr.push(datatmpYlqr);
      }

      this.graphCI = {
        data: dataYlqr,
        layout: this.layout_CI(),
      };
      this.yLQR.push(this.graphCI.data), console.log('yLQR', this.yLQR);
      console.log('graph.data', this.graphCI.data);
      this.codes.lqr = this.getCodeLQR(matriz_custo_lqr, data);
    });
  }

  calc_lqi() {
    this.panelCalc_lqi = true;
    this.panelCalc_lqr = false;
    this.panelCalc_lqg = false;
    this.panelCalc_lqgi = false;
    const matriz_custo_lqi = {
      A: this.matrizes[0].values,
      B: this.matrizes[1].values,
      C: this.matrizes[2].values,
      // D: this.matrizes[3].values,
      Q: this.matriz_custo[0].values,
      R: this.matriz_custo[1].values,
      CI: this.initialCond[0].values,
    };
    console.log('Matriz_custo_lqi:', matriz_custo_lqi);

    this.timeControllerDomainService.calc_lqi(matriz_custo_lqi).then((data) => {
      console.log(data);

      // @ts-ignore
      this.Nx = JSON.parse(data['Nx']);
      // @ts-ignore
      this.Ny = JSON.parse(data['Ny']);
      // @ts-ignore
      this.Nu = JSON.parse(data['Nu']);
      // @ts-ignore
      this.T = JSON.parse(data['T']);
      // @ts-ignore
      this.K = JSON.parse(data['K']);
      // @ts-ignore
      this.Ki = JSON.parse(data['Ki']);

      this.yLQI = [];
      this.uLQI = [];
      // @ts-ignore
      this.u_enc = data['Uhat'];
      this.u_lqi = JSON.parse(this.u_enc);
      console.log('u_lqi', this.u_lqi);
      // @ts-ignore
      this.y_enc = data['Yout'];
      this.y_lqi = JSON.parse(this.y_enc);
      console.log('y_lqi:', this.y_lqi);
      // @ts-ignore
      const vTime = data['time'];
      var dataUlqi = [];

      for (let i = 0; i < this.u_lqi.length; i++) {
        // (this.graph = {
        //   data: [
        //     {
        //       x: vTime,
        //       y: this.u_lqi[i],
        //       mode: 'lines',
        //       connectgaps: true,
        //       marker: { color: 'blue' },
        //     },
        //   ],
        //   layout: this.layout(),
        // }),
        //   this.uLQI.push(this.graph.data);
        // console.log('graph.data_LQI', this.graph.data);
        var datatmpUlqi = {
          x: vTime,
          y: this.u_lqi[i],
          mode: 'lines',
          type: 'scatter',
          connectgaps: true,
          name: `u${i + 1}`,
        };
        dataUlqi.push(datatmpUlqi);
      }

      this.graphCI = {
        data: dataUlqi,
        layout: this.layout_CI(),
      };
      this.uLQI.push(this.graphCI.data);

      console.log('uLQI', this.uLQI);

      var dataYlqi = [];
      for (let i = 0; i < this.y_lqi.length; i++) {
        // (this.graph = {
        //   data: [
        //     {
        //       x: vTime,
        //       y: this.y_lqi[i],
        //       mode: 'lines',
        //       connectgaps: true,
        //       marker: { color: 'blue' },
        //     },
        //   ],
        //   layout: this.layout(),
        // }),
        //   this.yLQI.push(this.graph.data),
        //   console.log('graph.data', this.graph.data);
        var datatmpYlqi = {
          x: vTime,
          y: this.y_lqi[i],
          mode: 'lines',
          type: 'scatter',
          connectgaps: true,
          name: `y${i + 1}`,
        };
        dataYlqi.push(datatmpYlqi);
      }

      this.graphCI = {
        data: dataYlqi,
        layout: this.layout_CI(),
      };
      this.yLQI.push(this.graphCI.data);
      console.log('yLQI', this.yLQI);
      this.codes.lqi = this.getCodeLQI(matriz_custo_lqi, data);
    });
  }

  calc_lqg() {
    this.panelCalc_lqg = true;
    this.panelCalc_lqr = false;
    this.panelCalc_lqi = false;
    this.panelCalc_lqgi = false;
    const matriz_custo_lqg = {
      A: this.matrizes[0].values,
      B: this.matrizes[1].values,
      C: this.matrizes[2].values,
      // D: this.matrizes[3].values,
      CI: this.initialCond[0].values,
      Q: this.matriz_custo[0].values,
      R: this.matriz_custo[1].values,
      QN: this.matriz_kalman[0].values,
      RN: this.matriz_kalman[1].values,
    };
    console.log('Matriz_custo_lqg:', matriz_custo_lqg);

    this.timeControllerDomainService.calc_lqg(matriz_custo_lqg).then((data) => {
      console.log(data);

      // @ts-ignore
      this.Nx = JSON.parse(data['Nx']);
      // @ts-ignore
      this.Ny = JSON.parse(data['Ny']);
      // @ts-ignore
      this.Nu = JSON.parse(data['Nu']);
      // @ts-ignore
      this.T = JSON.parse(data['T']);
      // @ts-ignore
      this.K = JSON.parse(data['K']);
      // @ts-ignore
      this.L = JSON.parse(data['L']);

      this.yLQG = [];
      this.uLQG = [];
      // @ts-ignore
      this.u_enc = data['Uhat'];
      this.u_lqg = JSON.parse(this.u_enc);
      console.log('u_lqg', this.u_lqg);

      // @ts-ignore
      this.y_enc = data['Yout'];
      this.y_lqg = JSON.parse(this.y_enc);
      console.log('y_lqg:', this.y_lqg);
      // @ts-ignore
      const vTime = data['time'];

      var dataYlqg = [];
      for (let i = 0; i < this.y_lqg.length; i++) {
        // (this.graph = {
        //   data: [
        //     {
        //       x: vTime,
        //       y: this.y_lqg[i],
        //       mode: 'lines',
        //       connectgaps: true,
        //       marker: { color: 'blue' },
        //     },
        //   ],
        //   layout: this.layout(),
        // }),
        //   this.yLQG.push(this.graph.data);
        // console.log('graph.data_LQG', this.graph.data);
        var datatmpYlqg = {
          x: vTime,
          y: this.y_lqg[i],
          mode: 'lines',
          type: 'scatter',
          connectgaps: true,
          name: `y${i + 1}`,
        };
        dataYlqg.push(datatmpYlqg);
      }

      this.graphCI = {
        data: dataYlqg,
        layout: this.layout_CI(),
      };
      this.yLQG.push(this.graphCI.data);

      console.log('yLQG', this.yLQG);

      var dataUlqg = [];
      for (let i = 0; i < this.u_lqg.length; i++) {
        // (this.graph = {
        //   data: [
        //     {
        //       x: vTime,
        //       y: this.u_lqg[i],
        //       mode: 'lines',
        //       connectgaps: true,
        //       marker: { color: 'blue' },
        //     },
        //   ],
        //   layout: this.layout(),
        // }),
        //   this.uLQG.push(this.graph.data),
        //   console.log('graph.data', this.graph.data);
        var datatmpUlqg = {
          x: vTime,
          y: this.u_lqg[i],
          mode: 'lines',
          type: 'scatter',
          connectgaps: true,
          name: `u${i + 1}`,
        };
        dataUlqg.push(datatmpUlqg);
      }

      this.graphCI = {
        data: dataUlqg,
        layout: this.layout_CI(),
      };
      this.uLQG.push(this.graphCI.data);
      console.log('uLQG', this.uLQG);
      this.codes.lqg = this.getCodeLQG(matriz_custo_lqg, data);
    });
  }

  calc_lqgi() {
    this.panelCalc_lqgi = true;
    this.panelCalc_lqr = false;
    this.panelCalc_lqi = false;
    this.panelCalc_lqg = false;
    const matriz_custo_lqgi = {
      A: this.matrizes[0].values,
      B: this.matrizes[1].values,
      C: this.matrizes[2].values,
      // D: this.matrizes[3].values,
      CI: this.initialCond[0].values,
      Q: this.matriz_custo[0].values,
      R: this.matriz_custo[1].values,
      QN: this.matriz_kalman[0].values,
      RN: this.matriz_kalman[1].values,
    };
    console.log('Matriz_custo_lqgi:', matriz_custo_lqgi);

    this.timeControllerDomainService.calc_lqgi(matriz_custo_lqgi).then(
      (data) => {
        console.log(data);

        // @ts-ignore
        this.Nx = JSON.parse(data['Nx']);
        // @ts-ignore
        this.Ny = JSON.parse(data['Ny']);
        // @ts-ignore
        this.Nu = JSON.parse(data['Nu']);
        // @ts-ignore
        this.T = JSON.parse(data['T']);
        // @ts-ignore
        this.K = JSON.parse(data['K']);
        // @ts-ignore
        this.Ki = JSON.parse(data['Ki']);
        // @ts-ignore
        this.L = JSON.parse(data['L']);

        this.yLQGI = [];
        this.uLQGI = [];
        // @ts-ignore
        this.u_enc = data['Uhat'];
        this.u_lqgi = JSON.parse(this.u_enc);
        console.log('u_lqgi', this.u_lqgi);

        // @ts-ignore
        this.y_enc = data['Yout'];
        this.y_lqgi = JSON.parse(this.y_enc);
        console.log('y_lqgi:', this.y_lqgi);
        // @ts-ignore
        const vTime = data['time'];

        var dataYlqgi = [];
        for (let i = 0; i < this.y_lqgi.length; i++) {
          // (this.graph = {
          //   data: [
          //     {
          //       x: vTime,
          //       y: this.y_lqgi[i],
          //       mode: 'lines',
          //       connectgaps: true,
          //       marker: { color: 'blue' },
          //     },
          //   ],
          //   layout: this.layout(),
          // }),
          //   this.yLQGI.push(this.graph.data);
          // console.log('graph.data_LQGI', this.graph.data);
          var datatmpYlqgi = {
            x: vTime,
            y: this.y_lqgi[i],
            mode: 'lines',
            type: 'scatter',
            connectgaps: true,
            name: `y${i + 1}`,
          };
          dataYlqgi.push(datatmpYlqgi);
        }

        this.graphCI = {
          data: dataYlqgi,
          layout: this.layout_CI(),
        };
        this.yLQGI.push(this.graphCI.data);
        console.log('yLQGI', this.yLQGI);

        var dataUlqgi = [];
        for (let i = 0; i < this.u_lqgi.length; i++) {
          // (this.graph = {
          //   data: [
          //     {
          //       x: vTime,
          //       y: this.u_lqgi[i],
          //       mode: 'lines',
          //       connectgaps: true,
          //       marker: { color: 'blue' },
          //     },
          //   ],
          //   layout: this.layout(),
          // }),
          //   this.uLQGI.push(this.graph.data),
          //   console.log('graph.data', this.graph.data);
          var datatmpUlqgi = {
            x: vTime,
            y: this.u_lqgi[i],
            mode: 'lines',
            type: 'scatter',
            connectgaps: true,
            name: `u${i + 1}`,
          };
          dataUlqgi.push(datatmpUlqgi);
        }

        this.graphCI = {
          data: dataUlqgi,
          layout: this.layout_CI(),
        };
        this.uLQGI.push(this.graphCI.data);
        console.log('uLQGI', this.uLQGI);
        this.codes.lqgi = this.getCodeLQGI(matriz_custo_lqgi, data);
        console.log('codes: ', this.codes);
      },
      (err) => {
        console.log(err);
        Swal.fire({
          title: 'Algoritmo não converge',
          text: 'Resintonizar as matrizes Q e/ou R!',
          icon: 'warning',
        });
      }
    );
  }

  calc() {
    this.panelMA = true;
    for (let i = 0; i < this.matrizes.length; i++) {
      console.log(
        'Calcular matrix ',
        this.matrizes[i].label,
        this.matrizes[i].values
      );
    }

    const input = {
      A: this.matrizes[0].values,
      B: this.matrizes[1].values,
      C: this.matrizes[2].values,
      // D: this.matrizes[3].values,
    };

    console.log('Input :: ', input);

    this.timeControllerDomainService.calcStep(input).then(
      (data) => {
        console.log(data);
        // @ts-ignore
        this.control_rank = data['control_rank'];
        // @ts-ignore
        this.obsv_rank = data['obsv_rank'];
        console.log(this.obsv_rank);

        this.stepMA = [];
        //const vY = data['outY_total'];
        // @ts-ignore
        this.vY = data['outY_total'];
        console.log('vY:', this.vY);
        // @ts-ignore
        const vTime = data['time'];

        var datas = [];
        this.lineNameIndex = 0;
        let outIndex = 0;
        for (let i = 0; i < this.vY.length; i++) {
          //   (this.graph = {
          //     data: [
          //       {
          //         x: vTime,
          //         y: this.vY[i],
          //         mode: 'lines',
          //         connectgaps: true,
          //         marker: { color: 'blue' },
          //       },
          //     ],
          //     layout: this.layout(),
          //   }),
          //     this.vY_linha.push(this.graph.data),
          //     console.log('graph.data', this.graph.data);
          // }
          var datatmp = {
            x: vTime,
            y: this.vY[i],
            mode: 'lines',
            type: 'scatter',
            connectgaps: true,
            name: this.getLineName(i + 1, outIndex),
          };
          datas.push(datatmp);
          if (this.lineNameIndex == this.outM) {
            this.lineNameIndex = 0;
            if (this.outM > this.inL) {
              outIndex += this.outM - this.inL;
            }
            if (this.outM == 1) {
              outIndex = 0;
            } else {
              outIndex++;
            }
          }
        }

        this.graph = {
          data: datas,
          layout: this.layout(),
        };
        this.stepMA.push(this.graph.data);
        console.log('graph.data', this.graph.data);
      },
      (err) => {
        console.log(err);
        Swal.fire(
          'Algoritmo não converge. \nResintonizar as matrizes Q e/ou R!'
        );
      }
    );
  }

  getLineName(index: number, outIndex: number) {
    return `De u${index - this.lineNameIndex - outIndex} para y${++this
      .lineNameIndex}`;
  }

  layout() {
    return this.layout_title('Resposta ao degrau unitário');
  }

  layout_title(title: string) {
    return {
      title: title,
      titlefont: {
        family: 'Arial, sans-serif',
        size: 12,
        color: 'black',
      },
      xaxis: {
        title: 'Tempo',
        titlefont: {
          family: 'Arial, sans-serif',
          size: 12,
          color: 'black',
        },
        showticklabels: true,
        tickangle: 'auto',
        tickfont: {
          family: 'Old Standard TT, serif',
          size: 12,
          color: 'black',
        },
      },
      yaxis: {
        title: 'Amplitude',
        titlefont: {
          family: 'Arial, sans-serif',
          size: 12,
          color: 'black',
        },
        showticklabels: true,
        tickangle: 45,
        tickfont: {
          family: 'Old Standard TT, serif',
          size: 12,
          color: 'black',
        },
        exponentformat: 'e',
        showexponent: 'all',
      },
    };
  }

  layout_CI() {
    return this.layout_title_CI('Resposta à condição inicial');
  }

  layout_title_CI(title: string) {
    return {
      title: title,
      titlefont: {
        family: 'Arial, sans-serif',
        size: 12,
        color: 'black',
      },
      xaxis: {
        title: 'Tempo',
        titlefont: {
          family: 'Arial, sans-serif',
          size: 12,
          color: 'black',
        },
        showticklabels: true,
        tickangle: 'auto',
        tickfont: {
          family: 'Old Standard TT, serif',
          size: 12,
          color: 'black',
        },
      },
      yaxis: {
        title: 'Amplitude',
        titlefont: {
          family: 'Arial, sans-serif',
          size: 12,
          color: 'black',
        },
        showticklabels: true,
        tickangle: 45,
        tickfont: {
          family: 'Old Standard TT, serif',
          size: 12,
          color: 'black',
        },
        exponentformat: 'e',
        showexponent: 'all',
      },
    };
  }

  costMatrixLqr() {
    this.panelCostMatrixLQR = true;
    this.panelCostMatrixLQI = false;
    this.panelCostMatrixLQG = false;
    this.panelCostMatrixLQGI = false;

    for (let i = 0; i < this.initialCond.length; i++) {
      const CI = this.initialCond[i];
      if (CI.label === 'CI') {
        CI.lines = 1;
        CI.cols = this.quadN;
      }
      for (let i = 0; i < CI.lines; i++) {
        for (let j = 0; j < CI.cols; j++) {
          CI.values[i][j] = 0;
        }
      }
    }
    for (let i = 0; i < this.matriz_custo.length; i++) {
      const myLQR = this.matriz_custo[i];
      if (myLQR.label === 'CI') {
        myLQR.lines = 1;
        myLQR.cols = this.quadN;
      }
      if (myLQR.label === 'Q') {
        myLQR.lines = this.quadN;
        myLQR.cols = this.quadN;
      }
      if (myLQR.label === 'R') {
        myLQR.lines = this.inL;
        myLQR.cols = this.inL;
      }
      myLQR.values = Array.from(
        Array(myLQR.lines),
        () => new Array(myLQR.cols)
      );
      for (let i = 0; i < myLQR.lines; i++) {
        for (let j = 0; j < myLQR.cols; j++) {
          myLQR.values[i][j] = 0;
        }
      }
      console.log('matriz_custo:', this.matriz_custo);
      console.log('myLQR:', myLQR);
    }
  }

  costMatrixLqi() {
    this.panelCostMatrixLQI = true;
    this.panelCostMatrixLQR = false;
    this.panelCostMatrixLQG = false;
    this.panelCostMatrixLQGI = false;

    for (let i = 0; i < this.initialCond.length; i++) {
      const CI = this.initialCond[i];
      if (CI.label === 'CI') {
        CI.lines = 1;
        CI.cols = this.quadN;
      }
      for (let i = 0; i < CI.lines; i++) {
        for (let j = 0; j < CI.cols; j++) {
          CI.values[i][j] = 0;
        }
      }
    }
    for (let i = 0; i < this.matriz_custo.length; i++) {
      const myLQI = this.matriz_custo[i];
      if (myLQI.label === 'CI') {
        myLQI.lines = 1;
        myLQI.cols = this.quadN;
      }
      if (myLQI.label === 'Q') {
        // if (this.inL > 1 && this.outM > 1) {
        if (this.inL === this.outM) {
          myLQI.lines = this.quadN + this.inL;
          myLQI.cols = this.quadN + this.inL;
        } else if (this.inL < this.outM) {
          myLQI.lines = this.quadN + this.outM;
          myLQI.cols = this.quadN + this.outM;
        } else {
          // (this.inL === 1 && this.outM === 1){
          myLQI.lines = this.quadN + 1;
          myLQI.cols = this.quadN + 1;
        }
        // myLQI.lines = this.quadN + this.inL;
        // myLQI.cols = this.quadN + this.inL;
      }
      if (myLQI.label === 'R') {
        myLQI.lines = this.inL;
        myLQI.cols = this.inL;
      }
      myLQI.values = Array.from(
        Array(myLQI.lines),
        () => new Array(myLQI.cols)
      );
      for (let i = 0; i < myLQI.lines; i++) {
        for (let j = 0; j < myLQI.cols; j++) {
          myLQI.values[i][j] = 0;
        }
      }
      console.log('matriz_custo:', this.matriz_custo);
      console.log('myLQI:', myLQI);
    }
    // })
  }

  costMatrixLqg() {
    this.panelCostMatrixLQG = true;
    this.panelCostMatrixLQR = false;
    this.panelCostMatrixLQI = false;
    this.panelCostMatrixLQGI = false;
    for (let i = 0; i < this.initialCond.length; i++) {
      const CI = this.initialCond[i];
      if (CI.label === 'CI') {
        CI.lines = 1;
        CI.cols = this.quadN;
      }
      for (let i = 0; i < CI.lines; i++) {
        for (let j = 0; j < CI.cols; j++) {
          CI.values[i][j] = 0;
        }
      }
    }
    for (let i = 0; i < this.matriz_custo.length; i++) {
      const myLQG = this.matriz_custo[i];
      if (myLQG.label === 'Q') {
        myLQG.lines = this.quadN;
        myLQG.cols = this.quadN;
      }
      if (myLQG.label === 'R') {
        myLQG.lines = this.inL;
        myLQG.cols = this.inL;
      }
      myLQG.values = Array.from(
        Array(myLQG.lines),
        () => new Array(myLQG.cols)
      );
      for (let i = 0; i < myLQG.lines; i++) {
        for (let j = 0; j < myLQG.cols; j++) {
          myLQG.values[i][j] = 0;
        }
      }
      console.log('matriz_custo:', this.matriz_custo);
      console.log('myLQG:', myLQG);
    }

    for (let i = 0; i < this.matriz_kalman.length; i++) {
      const myKalman = this.matriz_kalman[i];
      if (myKalman.label === 'QN') {
        myKalman.lines = this.inL;
        myKalman.cols = this.inL;
      }
      if (myKalman.label === 'RN') {
        myKalman.lines = this.outM;
        myKalman.cols = this.outM;
      }
      myKalman.values = Array.from(
        Array(myKalman.lines),
        () => new Array(myKalman.cols)
      );
      for (let i = 0; i < myKalman.lines; i++) {
        for (let j = 0; j < myKalman.cols; j++) {
          myKalman.values[i][j] = 0;
        }
      }
      console.log('matriz_kalman:', this.matriz_kalman);
      console.log('myLQG:', myKalman);
    }
  }

  costMatrixLqgi() {
    this.panelCostMatrixLQGI = true;
    this.panelCostMatrixLQR = false;
    this.panelCostMatrixLQI = false;
    this.panelCostMatrixLQG = false;
    for (let i = 0; i < this.initialCond.length; i++) {
      const LQGI_CI = this.initialCond[i];
      if (LQGI_CI.label === 'CI') {
        LQGI_CI.lines = 1;
        LQGI_CI.cols = this.quadN;
      }
      for (let i = 0; i < LQGI_CI.lines; i++) {
        for (let j = 0; j < LQGI_CI.cols; j++) {
          LQGI_CI.values[i][j] = 0;
        }
      }
    }
    for (let i = 0; i < this.matriz_custo.length; i++) {
      const myLQGI = this.matriz_custo[i];
      if (myLQGI.label === 'Q') {
        if (this.inL === this.outM) {
          myLQGI.lines = this.quadN + this.inL;
          myLQGI.cols = this.quadN + this.inL;
        } else if (this.inL < this.outM) {
          myLQGI.lines = this.quadN + this.outM;
          myLQGI.cols = this.quadN + this.outM;
        } else {
          // (this.inL === 1 && this.outM === 1){
          myLQGI.lines = this.quadN + 1;
          myLQGI.cols = this.quadN + 1;
        }
      }
      if (myLQGI.label === 'R') {
        myLQGI.lines = this.inL;
        myLQGI.cols = this.inL;
      }
      myLQGI.values = Array.from(
        Array(myLQGI.lines),
        () => new Array(myLQGI.cols)
      );
      for (let i = 0; i < myLQGI.lines; i++) {
        for (let j = 0; j < myLQGI.cols; j++) {
          myLQGI.values[i][j] = 0;
        }
      }
      console.log('matriz_custo:', this.matriz_custo);
      console.log('myLQGI:', myLQGI);
    }

    for (let i = 0; i < this.matriz_kalman.length; i++) {
      const myKalman = this.matriz_kalman[i];
      if (myKalman.label === 'QN') {
        myKalman.lines = this.inL;
        myKalman.cols = this.inL;
      }
      if (myKalman.label === 'RN') {
        myKalman.lines = this.outM;
        myKalman.cols = this.outM;
      }
      myKalman.values = Array.from(
        Array(myKalman.lines),
        () => new Array(myKalman.cols)
      );
      for (let i = 0; i < myKalman.lines; i++) {
        for (let j = 0; j < myKalman.cols; j++) {
          myKalman.values[i][j] = 0;
        }
      }
      console.log('matriz_kalman:', this.matriz_kalman);
      console.log('myLQG:', myKalman);
    }
  }

  codeCopied() {
    Swal.fire({
      position: 'center',
      icon: 'success',
      text: 'Seu código foi copiado!',
      showConfirmButton: false,
      timer: 1500,
    });
  }

  getCodeLQR(matriz_custo_lqr: any, data: Object) {
    return `
// *********************************************** //
//   Código gerado por EasyController for Arduino  //
//              www.easycontroller.com             //
// Usar com Arduinos baseados em processadores AVR //
// *********************************************** //

#include <TimerOne.h>
#include <BasicLinearAlgebra.h>

using namespace BLA;


// Declaração das variáveis de leitura
#define Nx ${this.Nx}        // Ordem da planta
#define Nu ${this.Nu}        // Número de sinais de controle
#define T  ${this.T}         // Período de amostragem [s]

// Inicialização dos vetores e matrizes
  // Matriz de ganhos (modificar aqui)
    BLA::Matrix<Nu, Nx> K = {${this.K}};
  // Vetor de estados (modificar condições inicias, se necessário)
    BLA::Matrix<Nx> x = {${matriz_custo_lqr.CI}};
  // Vetor de sinais de controle
    BLA::Matrix<Nu> u;
  // Vetor de PWM dos sinais de controle
    BLA::Matrix<Nu> u_pwm;
  // Saturação superior do sinal de controle (modificar aqui)
    BLA::Matrix<Nu> lim_sup = {1 , 1};
  // Saturação inferior do sinal de controle (modificar aqui)
    BLA::Matrix<Nu> lim_inf = {0 , 0};
  // Valor máximo do PWM (modificar aqui)
    BLA::Matrix<Nu> maxPWM = {255 , 255};
  // Valor mínimo do PWM (modificar aqui)
    BLA::Matrix<Nu> minPWM = {0 , 0};
  // Pinos de saída PWM (modificar aqui)
    BLA::Matrix<Nu> PWM_pins = {5 , 6};


// Inicializações de programa
int i=0, j=0, k=0;


double mapf(double val,double in_min,double in_max,double out_min,double out_max) {
  return (val-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}

// Setup
void setup()
{
  Timer1.initialize(1000000*T);      // Inicializa Timer1 com período de amostragem (em us)
  Timer1.attachInterrupt(controle);  // Define a interrupção de tempo
}


// Interrupção de tempo
void controle() {

  u = -K * x;

  // Calcula os sinais de controle saturados
  for (i = 0; i < Nu; i++) {
    if (u(i) > lim_sup(i)){
      u(i) = lim_sup(i);
    } else if (u(i) < lim_inf(i)) {
      u(i) = lim_inf(i);
    }
  }
}


void loop() {

  // Escrever aqui as leituras, conversões de sinal, etc.
  x(0) = analogRead(A0)*5/1023 -2;
  x(1) = analogRead(A1)*16/1023 -8;
  //x(2) = ...


  // Mapeamento (float) dos sinais de controle para as saídas PWM
  for (j = 0; j < Nu; j++) {
    u_pwm(j) = mapf(u(j),lim_inf(j),lim_sup(j),minPWM(j),maxPWM(j));
  }

  // Atualizaçãod dos PWM
  for (k = 0; k < Nu; k++) {
    analogWrite(PWM_pins(k),u_pwm(k));
  }
  `;
  }

  getCodeLQI(matriz_custo_lqi: any, data: Object) {
    return `
// *********************************************** //
//   Código gerado por EasyController for Arduino  //
//              www.easycontroller.com             //
// Usar com Arduinos baseados em processadores AVR //
// *********************************************** //

#include <TimerOne.h>
#include <BasicLinearAlgebra.h>

using namespace BLA;


// Declaração das variáveis de leitura
#define Nx ${this.Nx}        // Ordem da planta
#define Nu ${this.Nu}        // Número de sinais de controle
#define Ny ${this.Ny}        // Número de saídas
#define T  ${this.T}         // Período de amostragem [s]

// Inicialização dos vetores e matrizes
  // Matriz de saídas;
    BLA::Matrix<Ny, Nx> C = {${matriz_custo_lqi.C}};
  // Matriz de ganhos (modificar aqui)
    BLA::Matrix<Nu, Nx> K = {${this.K}};
    BLA::Matrix<Nu, Nx> Ki = {${this.Ki}};
    // Vetor de estados (modificar condições inicias, se necessário)
    BLA::Matrix<Nx> x = {${matriz_custo_lqi.CI}};
  // Vetor de sinais de controle
    BLA::Matrix<Nu> u;
  // Vetores para o integrador
    BLA::Matrix<Ny> y;
    BLA::Matrix<Ny> Ref;
    BLA::Matrix<Ny> int_e;
    BLA::Matrix<Ny> e;
  // Vetor de PWM dos sinais de controle
    BLA::Matrix<Nu> u_pwm;
  // Saturação superior do sinal de controle (modificar aqui)
    BLA::Matrix<Nu> lim_sup = {1 , 1};
  // Saturação inferior do sinal de controle (modificar aqui)
    BLA::Matrix<Nu> lim_inf = {0 , 0};
  // Valor máximo do PWM (modificar aqui)
    BLA::Matrix<Nu> maxPWM = {255 , 255};
  // Valor mínimo do PWM (modificar aqui)
    BLA::Matrix<Nu> minPWM = {0 , 0};
  // Pinos de saída PWM (modificar aqui)
    BLA::Matrix<Nu> PWM_pins = {5 , 6};


// Inicializações de programa
int i=0, j=0, k=0;


double mapf(double val,double in_min,double in_max,double out_min,double out_max) {
  return (val-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}

// Setup
void setup()
{
  Timer1.initialize(1000000*T);      // Inicializa Timer1 com período de amostragem (em us)
  Timer1.attachInterrupt(controle);  // Define a interrupção de tempo
}


// Interrupção de tempo
void controle() {

  y = C * x;
  e = Ref - y;
  int_e = int_e + e * T;
  u = -K * x - Ki * int_e;

  // Calcula os sinais de controle saturados
  for (i = 0; i < Nu; i++) {
    if (u(i) > lim_sup(i)){
      u(i) = lim_sup(i);
    } else if (u(i) < lim_inf(i)) {
      u(i) = lim_inf(i);
    }
  }
}


void loop() {

  // Escrever aqui as leituras, conversões de sinal, etc.
  x(0) = analogRead(A0)*5/1023 -2;
  x(1) = analogRead(A1)*16/1023 -8;
  //x(2) = ...


  // Mapeamento (float) dos sinais de controle para as saídas PWM
  for (j = 0; j < Nu; j++) {
    u_pwm(j) = mapf(u(j),lim_inf(j),lim_sup(j),minPWM(j),maxPWM(j));
  }

  // Atualizaçãod dos PWM
  for (k = 0; k < Nu; k++) {
    analogWrite(PWM_pins(k),u_pwm(k));
  }
  `;
  }

  getCodeLQG(matriz_custo_lqg: any, data: Object) {
    return `
// *********************************************** //
//   Código gerado por EasyController for Arduino  //
//              www.easycontroller.com             //
// Usar com Arduinos baseados em processadores AVR //
// *********************************************** //

#include <TimerOne.h>
#include <BasicLinearAlgebra.h>

using namespace BLA;


// Declaração das variáveis de leitura
#define Nx ${this.Nx}        // Ordem da planta
#define Nu ${this.Nu}        // Número de sinais de controle
#define Ny ${this.Ny}        // Número de saídas
#define T  ${this.T}     // Período de amostragem [s]

// Inicialização dos vetores e matrizes
  // Matriz de estados
    BLA::Matrix<Nx, Nx> A = {${matriz_custo_lqg.A}};
  // Matrix de entradas
    BLA::Matrix<Nx, Nu> B = {${matriz_custo_lqg.B}};
  // Matrix de saídas
    BLA::Matrix<Ny, Nx> C = {${matriz_custo_lqg.C}};
  // Matriz de ganhos (modificar aqui)
    BLA::Matrix<Nu, Nx> K = {${this.K}};
  // Matrix de ganhos de Kalman
    BLA::Matrix<Nx, Nx> L = {${this.L}};
  // Vetor de estados (modificar condições inicias, se necessário)
    BLA::Matrix<Nx, Nx> x = {${matriz_custo_lqg.CI}};
  // Vetor de sinais de controle
    BLA::Matrix<Nu, Nu> u;
  // Vetor  de saídas
    BLA::Matrix<Ny, Ny> y;
  // Vetor de estados estimados
    BLA::Matrix<Nx, Nx> xhat;
  // Vetor de PWM dos sinais de controle
    BLA::Matrix<Nu> u_pwm;
  // Saturação superior do sinal de controle (modificar aqui)
    BLA::Matrix<Nu> lim_sup = {1 , 1};
  // Saturação inferior do sinal de controle (modificar aqui)
    BLA::Matrix<Nu> lim_inf = {0 , 0};
  // Valor máximo do PWM (modificar aqui)
    BLA::Matrix<Nu> maxPWM = {255 , 255};
  // Valor mínimo do PWM (modificar aqui)
    BLA::Matrix<Nu> minPWM = {0 , 0};
  // Pinos de saída PWM (modificar aqui)
    BLA::Matrix<Nu> PWM_pins = {5 , 6};


// Inicializações de programa
int i=0, j=0, k=0;


double mapf(double val,double in_min,double in_max,double out_min,double out_max) {
  return (val-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}

// Setup
void setup()
{
  Timer1.initialize(1000000*T);      // Inicializa Timer1 com período de amostragem (em us)
  Timer1.attachInterrupt(controle);  // Define a interrupção de tempo
}


// Interrupção de tempo
void controle() {

  y = C * x;
  xhat = xhat + ((A - L * C) * xhat + (B * u) + (L * y)) * T;
  u = -K * xhat;

  // Calcula os sinais de controle saturados
  for (i = 0; i < Nu; i++) {
    if (u(i) > lim_sup(i)){
      u(i) = lim_sup(i);
    } else if (u(i) < lim_inf(i)) {
      u(i) = lim_inf(i);
    }
  }
}


void loop() {

  // Escrever aqui as leituras, conversões de sinal, etc.
  x(0) = analogRead(A0)*5/1023 -2;
  x(1) = analogRead(A1)*16/1023 -8;
  //x(2) = ...


  // Mapeamento (float) dos sinais de controle para as saídas PWM
  for (j = 0; j < Nu; j++) {
    u_pwm(j) = mapf(u(j),lim_inf(j),lim_sup(j),minPWM(j),maxPWM(j));
  }

  // Atualizaçãod dos PWM
  for (k = 0; k < Nu; k++) {
    analogWrite(PWM_pins(k),u_pwm(k));
  }
  `;
  }

  getCodeLQGI(matriz_custo_lqgi: any, data: Object) {
    return `

  // *********************************************** //
  //   Código gerado por EasyController for Arduino  //
  //              www.easycontroller.com             //
  // Usar com Arduinos baseados em processadores AVR //
  // *********************************************** //

  #include <TimerOne.h>
  #include <BasicLinearAlgebra.h>

  using namespace BLA;


  // Declaração das variáveis de leitura
  #define Nx ${this.Nx}        // Ordem da planta
  #define Nu ${this.Nu}        // Número de sinais de controle
  #define Ny ${this.Ny}        // Número de saídas
  #define T  ${this.T}         // Período de amostragem [s]

  // Inicialização dos vetores e matrizes
    // Matriz de estados
      BLA::Matrix<Nx, Nx> A = {${matriz_custo_lqgi.A}};
    // Matriz de entradas
      BLA::Matrix<Nx, Nu> B = {${matriz_custo_lqgi.B}};
    // Matriz de saídas
      BLA::Matrix<Ny, Nx> C = {${matriz_custo_lqgi.C}};
    // Matriz de ganhos (modificar aqui)
      BLA::Matrix<Nu, Nx> K = {${this.K}};
    // Matriz de ganhos do integrador
      BLA::Matrix<Nu, Ny> Ki = {${this.Ki}};
    // Matriz de ganhos de Kalman
      BLA::Matrix<Nx, Nx> L = {${this.L}};
    // Vetor de estados (modificar condições inicias, se necessário)
      BLA::Matrix<Nx, Nx> x = {${matriz_custo_lqgi.CI}};
    // Vetor de sinais de controle
      BLA::Matrix<Nu, Nu> u;
    // Vetor  de saídas
      BLA::Matrix<Ny, Ny> y;
    // Vetores para o integrador
      BLA::Matrix<Ny, Ny> Ref;
      BLA::Matrix<Ny, Ny> int_e;
      BLA::Matrix<Ny, Ny> e;
    // Vetor de estados estimados
      BLA::Matrix<Nx, Nx> xhat;
    // Vetor de PWM dos sinais de controle
      BLA::Matrix<Nu> u_pwm;
    // Saturação superior do sinal de controle (modificar aqui)
      BLA::Matrix<Nu> lim_sup = {1 , 1};
    // Saturação inferior do sinal de controle (modificar aqui)
      BLA::Matrix<Nu> lim_inf = {0 , 0};
    // Valor máximo do PWM (modificar aqui)
      BLA::Matrix<Nu> maxPWM = {255 , 255};
    // Valor mínimo do PWM (modificar aqui)
      BLA::Matrix<Nu> minPWM = {0 , 0};
    // Pinos de saída PWM (modificar aqui)
      BLA::Matrix<Nu> PWM_pins = {5 , 6};


  // Inicializações de programa
  int i=0, j=0, k=0;

  double mapf(double val,double in_min,double in_max,double out_min,double out_max) {
    return (val-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
  }

  // Setup
  void setup()
  {
    Timer1.initialize(1000000*T);      // Inicializa Timer1 com período de amostragem (em us)
    Timer1.attachInterrupt(controle);  // Define a interrupção de tempo
  }


  // Interrupção de tempo
  void controle() {

    y = C * x;
    e = Ref - y;
    int_e = int_e + e * T;
    xhat = xhat + ((A - L * C) * xhat + (B * u) + (L * y)) * T;
    u = -K * xhat - Ki * int_e;

    // Calcula os sinais de controle saturados
    for (i = 0; i < Nu; i++) {
      if (u(i) > lim_sup(i)){
        u(i) = lim_sup(i);
      } else if (u(i) < lim_inf(i)) {
        u(i) = lim_inf(i);
      }
    }
  }


  void loop() {

    // Escrever aqui as leituras, conversões de sinal, etc.
    x(0) = analogRead(A0)*5/1023 -2;
    x(1) = analogRead(A1)*16/1023 -8;
    //x(2) = ...


    // Mapeamento (float) dos sinais de controle para as saídas PWM
    for (j = 0; j < Nu; j++) {
      u_pwm(j) = mapf(u(j),lim_inf(j),lim_sup(j),minPWM(j),maxPWM(j));
    }

    // Atualização dos PWM
    for (k = 0; k < Nu; k++) {
      analogWrite(PWM_pins(k),u_pwm(k));
    };`;
  }
}

