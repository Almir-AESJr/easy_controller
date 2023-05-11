import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {firstValueFrom} from "rxjs";

@Injectable()
export class TimeControllerDomainService {

  constructor(private http: HttpClient) {
  }

  async calcStep(data: any) {
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': '*'
    };

    return await firstValueFrom(this.http.post('http://127.0.0.1:8000/easy-controller/', data, {headers}));
  }

  async calc_lqr(data: any) {
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': '*'
    };

    return await firstValueFrom(this.http.post('http://127.0.0.1:8000/easy-controller/lqr', data, {headers}));
  }

  async calc_lqi(data: any) {
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': '*'
    };

    return await firstValueFrom(this.http.post('http://127.0.0.1:8000/easy-controller/lqi', data, {headers}));
  }

  async calc_lqg(data: any) {
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': '*'
    };

    return await firstValueFrom(this.http.post('http://127.0.0.1:8000/easy-controller/lqg', data, {headers}));
  }

  async calc_lqgi(data: any) {
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': '*'
    };

    return await firstValueFrom(this.http.post('http://127.0.0.1:8000/easy-controller/lqgi', data, {headers}));
  }
}
