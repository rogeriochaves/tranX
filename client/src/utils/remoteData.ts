// Based on https://package.elm-lang.org/packages/krisajenkins/remotedata/6.0.1/RemoteData
export type RemoteData<T> =
  | { state: "NOT_ASKED" }
  | { state: "LOADING" }
  | { state: "FAILURE"; error: string }
  | { state: "SUCCESS"; data: T };

export function NotAsked<T>(): RemoteData<T> {
  return { state: "NOT_ASKED" };
}

export function Loading<T>(): RemoteData<T> {
  return { state: "LOADING" };
}

export function Failure<T>(error: string): RemoteData<T> {
  return { state: "FAILURE", error };
}

export function Success<T>(data: T): RemoteData<T> {
  return { state: "SUCCESS", data };
}
