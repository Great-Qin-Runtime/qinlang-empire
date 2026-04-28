% 律令郡 · Prolog 主程序
%
% 角色：service（trigger=event, listens_to=[dispute, tax-evasion]）
% 读 stdin JSON dispatch envelope，依 Horn 子句判定，写 stdout JSON delta。

:- use_module(library(http/json)).
:- initialization(main, main).

% ======== 律令子句（Horn rules） ========

verdict(dispute, dismissed, "讼小，戒而释之").
verdict(dispute, fined,     "讼大，罚以钱粮").
verdict('tax-evasion', fined, "逋税，加倍科其家").

% 由 (event_type, severity) 决定判决
judge(dispute,        S, dismissed) :- S =< 1, !.
judge(dispute,        _, fined).
judge('tax-evasion',  _, fined).

reward_for(dismissed, 0,   1).      % audits_passed +1
reward_for(fined,     5,   1).      % stats.reputation +1, treasury.qian-liang +5

% ======== 主流程 ========

main :-
    json_read_dict(user_input, Env, [tag(_)]),
    Dispatch = Env.dispatch,
    Tick = Dispatch.tick,
    DispatchId = Dispatch.dispatch_id,
    ( get_dict('event_queue', Dispatch, Events0) -> Events = Events0 ; Events = [] ),
    process_events(Events, 0, 0, 0, Verdicts),
    Verdicts = verdicts(QianLiang, Reputation, AuditsPassed, Texts),
    build_events(Texts, EventList),
    Out = _{
        language: "Prolog",
        province: "律令郡",
        ok: true,
        tick: Tick,
        dispatch_id: DispatchId,
        deltas: _{
            treasury: _{ 'qian-liang': QianLiang },
            stats: _{ reputation: Reputation, audits_passed: AuditsPassed }
        },
        events: EventList
    },
    json_write_dict(user_output, Out, [width(0)]),
    nl.

process_events([], QL, R, AP, verdicts(QL, R, AP, [])).
process_events([E|Es], QL, R, AP, verdicts(QL2, R2, AP2, [Text|Texts])) :-
    ( get_dict(type, E, TypeRaw) -> atom_string(Type, TypeRaw) ; Type = unknown ),
    ( get_dict(severity, E, SevRaw)
        -> ( number(SevRaw) -> Sev = SevRaw ; Sev = 1 )
        ;  Sev = 1 ),
    ( judge(Type, Sev, Verdict) -> true ; Verdict = dismissed ),
    ( verdict(Type, Verdict, MsgRaw) -> Msg = MsgRaw ; Msg = "无律可循" ),
    reward_for(Verdict, DQL, DR),
    ( Verdict == dismissed -> DAP = 1 ; DAP = 0 ),
    QLn is QL + DQL, Rn is R + DR, APn is AP + DAP,
    format(string(Text), "律令郡：~w → ~w（~w）", [Type, Verdict, Msg]),
    process_events(Es, QLn, Rn, APn, verdicts(QL2, R2, AP2, Texts)).

build_events([], []).
build_events([T|Ts], [_{type: "service", text: T, severity: "info"}|Es]) :-
    build_events(Ts, Es).
